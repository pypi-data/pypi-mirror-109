"""Feedback Evaluator
"""
import types
from typing import Optional

import torch
from torch import optim
from torch.autograd import Variable
from torch.nn import Parameter
import torch.nn.functional as F

import seqgra.constants as c
from seqgra.evaluator.gradientbased import AbstractGradientEvaluator
from seqgra.learner import Learner


class FeedbackEvaluator(AbstractGradientEvaluator):
    """Feedback evaluator for PyTorch models
    """
    def __init__(self, learner: Learner, output_dir: str,
                 importance_threshold: Optional[float] = None,
                 input_size=None, class_num=1000,
                 lr=0.1, lambd=0.01, max_iters=30,
                 silent: bool = False) -> None:
        super().__init__(c.EvaluatorID.FEEDBACK, "Feedback", learner,
                         output_dir, importance_threshold, silent=silent)
        self.lr = lr
        self.lambd = lambd
        self.max_iters = max_iters
        self.input_size = input_size
        self.class_num = class_num
        self.control_gates = []

        self._init_control_gates()
        self.learner.model.apply(replace_mask)

    def explain(self, x, y):
        self._reset_control_gates()
        optimizer = optim.SGD(self.control_gates, lr=self.lr,
                              momentum=0.9, weight_decay=0.0)

        mask = torch.zeros(self.input_size[0], self.class_num).to(self.learner.device)
        mask.scatter_(1, y.unsqueeze(1), 1)
        mask_var = Variable(mask)

        for j in range(self.max_iters):
            output = self.learner.model(x)
            loss = -(output * mask_var).sum()

            for v in self.control_gates:
                loss += self.lambd * v.abs().sum()

            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

            for v in self.control_gates:
                v.data.clamp_(0, 1)

        grad = self._backprop(x, y)
        return grad.abs()
        
    def _init_control_gates(self):
        self.learner.model.apply(replace_first)
        input_placeholder = Variable(
            torch.randn(*self.input_size).to(self.learner.device))
        _ = self.learner.model(input_placeholder)
        for m in self.learner.model.modules():
            if m.__class__.__name__ == 'ReLU':
                self.control_gates.append(m.control_gate)

    def _reset_control_gates(self):
        for i in range(len(self.control_gates)):
            self.control_gates[i].data.fill_(1.0)
            if self.control_gates[i].grad is not None:
                self.control_gates[i].grad.data.fill_(0.0)

def first_forward(self, x):
    out = F.relu(x)
    self.control_gate = Parameter(out.data.clone())
    self.control_gate.data.fill_(1.0)
    return out


def mask_forward(self, x):
    out = F.relu(x)
    out = self.control_gate * out
    return out


def replace_first(m):
    name = m.__class__.__name__
    if name.find('ReLU') != -1:
        m.forward = types.MethodType(first_forward, m)


def replace_mask(m):
    name = m.__class__.__name__
    if name.find('ReLU') != -1:
        m.forward = types.MethodType(mask_forward, m)

