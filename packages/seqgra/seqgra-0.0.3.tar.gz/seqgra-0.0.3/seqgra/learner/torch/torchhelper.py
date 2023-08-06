"""MIT - CSAIL - Gifford Lab - seqgra

PyTorch learner helper class

@author: Konstantin Krismer
"""
from ast import literal_eval
from distutils.util import strtobool
import importlib
import logging
import os
import random
import shutil
import sys
from typing import FrozenSet, List, Optional

from ignite.engine import Events
from ignite.engine import create_supervised_trainer
from ignite.engine import create_supervised_evaluator
from ignite.metrics import Accuracy, Loss
from ignite.handlers import EarlyStopping, ModelCheckpoint
import numpy as np
import pkg_resources
import torch

from seqgra import ModelSize
import seqgra.constants as c
from seqgra.learner import Learner


class TorchHelper:
    MULTI_CLASS_CLASSIFICATION_LOSSES: FrozenSet[str] = frozenset(
        ["crossentropyloss", "nllloss", "kldivloss", "hingeembeddingloss",
         "cosineembeddingloss"])

    MULTI_LABEL_CLASSIFICATION_LOSSES: FrozenSet[str] = frozenset(
        ["bcewithlogitsloss", "bceloss"])

    MULTIPLE_REGRESSION_LOSSES: FrozenSet[str] = frozenset(
        ["l1loss", "mseloss", "smoothl1loss"])

    MULTIVARIATE_REGRESSION_LOSSES: FrozenSet[str] = MULTIPLE_REGRESSION_LOSSES

    @staticmethod
    def create_model(learner: Learner) -> None:
        path = learner.definition.architecture.external_model_path
        class_name = learner.definition.architecture.external_model_class_name
        learner.set_seed()

        if path is None:
            raise Exception("embedded architecture definition not supported"
                            " for PyTorch models")
        elif path is not None and \
                learner.definition.architecture.external_model_format is not None:
            if learner.definition.architecture.external_model_format == "pytorch-module":
                if os.path.isfile(path):
                    if class_name is None:
                        raise Exception(
                            "PyTorch model class name not specified")
                    else:
                        module_spec = importlib.util.spec_from_file_location(
                            "model", path)
                        torch_model_module = importlib.util.module_from_spec(
                            module_spec)
                        module_spec.loader.exec_module(torch_model_module)
                        torch_model_class = getattr(torch_model_module,
                                                    class_name)
                        learner.model = torch_model_class()
                else:
                    raise Exception(
                        "PyTorch model class file does not exist: " + path)
            else:
                raise Exception(
                    "unsupported PyTorch model format: " +
                    learner.definition.architecture.external_model_format)
        else:
            raise Exception("neither internal nor external architecture "
                            "definition provided")

        if learner.definition.optimizer_hyperparameters is None:
            raise Exception("optimizer undefined")
        else:
            learner.optimizer = TorchHelper.get_optimizer(
                learner.definition.optimizer_hyperparameters,
                learner.model.parameters())

        if learner.definition.loss_hyperparameters is None:
            raise Exception("loss undefined")
        else:
            learner.criterion = TorchHelper.get_loss(
                learner.definition.loss_hyperparameters)

        if learner.metrics is None:
            raise Exception("metrics undefined")

    @staticmethod
    def print_model_summary(learner: Learner):
        if learner.model:
            print(learner.model)
        else:
            print("uninitialized model")

    @staticmethod
    def set_seed(learner: Learner) -> None:
        random.seed(learner.definition.seed)
        np.random.seed(learner.definition.seed)
        torch.manual_seed(learner.definition.seed)

    @staticmethod
    def train_model(
            learner: Learner,
            training_dataset: torch.utils.data.Dataset,
            validation_dataset: torch.utils.data.Dataset,
            output_layer_activation_function: Optional[str] = None,
            silent: bool = False) -> None:
        logger = logging.getLogger(__name__)
        if silent:
            logger.setLevel(os.environ.get("LOGLEVEL", "WARNING"))

        if learner.model is None:
            learner.create_model()

        # save number of model parameters
        num_trainable_params, num_non_trainable_params = learner.get_num_params()
        with open(learner.output_dir +
                  "num-model-parameters.txt", "w") as model_param_file:
            model_param_file.write("number of trainable parameters\t" +
                                   str(num_trainable_params) + "\n")
            model_param_file.write("number of non-trainable parameters\t" +
                                   str(num_non_trainable_params) + "\n")
            model_param_file.write("number of all parameters\t" +
                                   str(num_trainable_params +
                                       num_non_trainable_params) + "\n")

        batch_size = int(
            learner.definition.training_process_hyperparameters["batch_size"])

        # init data loaders
        if isinstance(training_dataset, torch.utils.data.IterableDataset):
            # examples are shuffled in IterableDataSet class
            shuffle: bool = False
        else:
            shuffle: bool = bool(
                strtobool(learner.definition.training_process_hyperparameters["shuffle"]))

        training_loader = torch.utils.data.DataLoader(
            training_dataset,
            batch_size=batch_size,
            shuffle=shuffle)

        validation_loader = torch.utils.data.DataLoader(
            validation_dataset,
            batch_size=batch_size,
            shuffle=False)

        # GPU or CPU?
        learner.model = learner.model.to(learner.device)
        logger.info("using device: %s", learner.device_label)

        # training loop
        trainer = create_supervised_trainer(learner.model, learner.optimizer,
                                            learner.criterion,
                                            device=learner.device)
        train_evaluator = create_supervised_evaluator(
            learner.model,
            metrics=TorchHelper.get_metrics(
                learner, output_layer_activation_function),
            device=learner.device)
        val_evaluator = create_supervised_evaluator(
            learner.model,
            metrics=TorchHelper.get_metrics(
                learner, output_layer_activation_function),
            device=learner.device)

        logging.getLogger("ignite.engine.engine.Engine").setLevel(
            logging.WARNING)

        num_epochs: int = int(
            learner.definition.training_process_hyperparameters["epochs"])

        @trainer.on(Events.EPOCH_COMPLETED)
        def log_training_results(trainer):
            logger.info("epoch {}/{}".format(trainer.state.epoch, num_epochs))
            train_evaluator.run(training_loader)
            metrics = train_evaluator.state.metrics
            logger.info(TorchHelper._format_metrics_output(
                metrics, "training set"))

        @trainer.on(Events.EPOCH_COMPLETED)
        def log_validation_results(trainer):
            val_evaluator.run(validation_loader)
            metrics = val_evaluator.state.metrics
            logger.info(TorchHelper._format_metrics_output(metrics,
                                                           "validation set"))

        @trainer.on(Events.EPOCH_COMPLETED)
        def log_last_epoch(trainer):
            with open(learner.output_dir + "last-epoch-completed.txt", "w") as last_epoch_file:
                last_epoch_file.write(str(trainer.state.epoch) + "\n")

        # save best model
        def score_fn(engine):
            if "loss" in learner.metrics:
                score = engine.state.metrics["loss"]
                score = -score
            elif "accuracy" in learner.metrics:
                score = engine.state.metrics["accuracy"]
            else:
                raise Exception("no metric to track performance")
            return score

        best_model_dir: str = learner.output_dir + "tmp"
        best_model_saver_handler = ModelCheckpoint(
            best_model_dir,
            score_function=score_fn,
            filename_prefix="best",
            n_saved=1,
            create_dir=True)
        val_evaluator.add_event_handler(Events.COMPLETED,
                                        best_model_saver_handler,
                                        {"model": learner.model})

        # early stopping callback
        if bool(strtobool(learner.definition.training_process_hyperparameters["early_stopping"])):
            if "early_stopping_patience" in learner.definition.training_process_hyperparameters:
                patience: int = int(
                    learner.definition.training_process_hyperparameters["early_stopping_patience"])
            else:
                patience: int = 10
            es_handler = EarlyStopping(patience=patience,
                                       score_function=score_fn,
                                       trainer=trainer,
                                       min_delta=0)
            val_evaluator.add_event_handler(Events.COMPLETED, es_handler)

        trainer.run(training_loader, max_epochs=num_epochs)

        # load best model after training
        best_model = TorchHelper.get_best_model_file_name(best_model_dir)
        if best_model:
            learner.load_model("tmp/" + best_model)
            # remove temp folder
            shutil.rmtree(best_model_dir)
        else:
            logger.warn("best model could not be loaded")

    @staticmethod
    def evaluate_model(learner: Learner, dataset: torch.utils.data.Dataset,
                       output_layer_activation_function: Optional[str] = None):
        data_loader = torch.utils.data.DataLoader(
            dataset,
            batch_size=int(
                learner.definition.training_process_hyperparameters["batch_size"]),
            shuffle=False)

        learner.model = learner.model.to(learner.device)

        running_loss: float = 0.0
        running_correct: int = 0
        num_examples: int = 0

        learner.model.eval()
        with torch.no_grad():
            for x, y in data_loader:
                # transfer to device
                x = x.to(learner.device)
                y = y.to(learner.device)

                y_hat = learner.model(x)
                loss = learner.criterion(y_hat, y)

                if output_layer_activation_function is not None:
                    if output_layer_activation_function == "softmax":
                        y_hat = torch.nn.functional.softmax(y_hat, dim=1)
                    elif output_layer_activation_function == "sigmoid":
                        y_hat = torch.sigmoid(y_hat)

                # binarize y_hat
                if learner.definition.task == c.TaskType.MULTI_CLASS_CLASSIFICATION:
                    indices = torch.argmax(y_hat, dim=1)
                    correct = torch.eq(indices, y).view(-1)
                elif learner.definition.task == c.TaskType.MULTI_LABEL_CLASSIFICATION:
                    y_hat = torch.gt(y_hat, 0.5)
                    y = y.type_as(y_hat)

                    correct = torch.all(y == y_hat, dim=-1)

                running_correct += torch.sum(correct).item()
                running_loss += loss.item() * x.size(0)
                num_examples += correct.shape[0]

        overall_loss = running_loss / num_examples
        overall_accuracy = running_correct / num_examples

        return {"loss": overall_loss, "accuracy": overall_accuracy}

    @staticmethod
    def predict(learner: Learner, dataset: torch.utils.data.Dataset,
                output_layer_activation_function: Optional[str] = None):
        """ This is the forward calculation from x to y
        Returns:
            softmax_linear: Output tensor with the computed logits.
        """
        data_loader = torch.utils.data.DataLoader(
            dataset,
            batch_size=int(
                learner.definition.training_process_hyperparameters["batch_size"]),
            shuffle=False)

        learner.model = learner.model.to(learner.device)

        y_hat = []
        learner.model.eval()
        with torch.no_grad():
            for x in data_loader:
                # transfer to device
                x = x.to(learner.device)

                raw_logits = learner.model(x)
                if output_layer_activation_function is None:
                    y_hat += raw_logits.tolist()
                elif output_layer_activation_function == "softmax":
                    y_hat += \
                        torch.nn.functional.softmax(raw_logits, dim=1).tolist()
                elif output_layer_activation_function == "sigmoid":
                    y_hat += torch.sigmoid(raw_logits).tolist()

        return np.array(y_hat)

    @staticmethod
    def get_best_model_file_name(best_model_dir: str) -> str:
        model_files = [model_file
                       for model_file in os.listdir(best_model_dir)
                       if model_file.endswith(".pth") or model_file.endswith(".pt")]
        if len(model_files) == 1:
            return model_files[0]
        else:
            return None

    @staticmethod
    def _format_metrics_output(metrics, set_label):
        message: List[str] = [set_label + " metrics:\n"]
        message += [" - " + metric + ": " + str(metrics[metric]) + "\n"
                    for metric in metrics]
        return "".join(message).rstrip()

    @staticmethod
    def train_model_basic(
            learner: Learner,
            training_dataset: torch.utils.data.Dataset,
            validation_dataset: torch.utils.data.Dataset,
            output_layer_activation_function: Optional[str] = None,
            silent: bool = False) -> None:
        logger = logging.getLogger(__name__)
        if silent:
            logger.setLevel(os.environ.get("LOGLEVEL", "WARNING"))

        if learner.model is None:
            learner.create_model()

        batch_size = int(
            learner.definition.training_process_hyperparameters["batch_size"])

        # init data loaders
        training_loader = torch.utils.data.DataLoader(
            training_dataset,
            batch_size=batch_size,
            shuffle=bool(strtobool(
                learner.definition.training_process_hyperparameters["shuffle"])))

        validation_loader = torch.utils.data.DataLoader(
            validation_dataset,
            batch_size=batch_size,
            shuffle=False)

        # GPU or CPU?
        learner.model = learner.model.to(learner.device)
        logger.info("using device: %s", learner.device_label)

        # training loop
        num_epochs: int = int(
            learner.definition.training_process_hyperparameters["epochs"])

        for epoch in range(num_epochs):
            logger.info("epoch {}/{}".format(epoch + 1, num_epochs))

            for phase in [c.DataSet.TRAINING, c.DataSet.VALIDATION]:
                if phase == c.DataSet.TRAINING:
                    learner.model.train()
                    data_loader = training_loader
                else:
                    learner.model.eval()
                    data_loader = validation_loader

                running_loss: float = 0.0
                running_correct: int = 0

                for x, y in data_loader:
                    # transfer to device
                    x = x.to(learner.device)
                    y = y.to(learner.device)

                    # zero the parameter gradients
                    learner.optimizer.zero_grad()

                    # forward
                    # track history if only in train
                    with torch.set_grad_enabled(phase == c.DataSet.TRAINING):
                        y_hat = learner.model(x)
                        loss = learner.criterion(y_hat, y)

                        # backward + optimize only if in training phase
                        if phase == c.DataSet.TRAINING:
                            loss.backward()
                            learner.optimizer.step()

                        if output_layer_activation_function is not None:
                            if output_layer_activation_function == "softmax":
                                y_hat = torch.nn.functional.softmax(
                                    y_hat, dim=1)
                            elif output_layer_activation_function == "sigmoid":
                                y_hat = torch.sigmoid(y_hat)

                        # statistics
                        if learner.definition.task == c.TaskType.MULTI_CLASS_CLASSIFICATION:
                            indices = torch.argmax(y_hat, dim=1)
                            correct = torch.eq(indices, y).view(-1)
                        elif learner.definition.task == c.TaskType.MULTI_LABEL_CLASSIFICATION:
                            # binarize y_hat
                            y_hat = torch.gt(y_hat, 0.5)
                            y = y.type_as(y_hat)

                            correct = torch.all(y == y_hat, dim=-1)

                        running_correct += torch.sum(correct).item()
                        running_loss += loss.item() * x.size(0)

                epoch_loss = running_loss / len(data_loader.dataset)
                epoch_acc = running_correct.float() / len(data_loader.dataset)

                logger.info("{} - loss: {:.3f}, accuracy: {:.3f}".format(
                    phase, epoch_loss, epoch_acc))

    @staticmethod
    def save_model(learner: Learner, file_name: Optional[str] = None) -> None:
        if not file_name:
            file_name = "saved_model.pth"

            # save session info
            learner.write_session_info()

        if os.path.dirname(file_name):
            os.makedirs(learner.output_dir + os.path.dirname(file_name))

        torch.save(learner.model.state_dict(), learner.output_dir + file_name)

    @staticmethod
    def write_session_info(learner: Learner) -> None:
        with open(learner.output_dir + "session-info.txt", "w") as session_file:
            session_file.write("seqgra package version: " +
                               pkg_resources.require("seqgra")[0].version + "\n")
            session_file.write("PyTorch version: " + torch.__version__ + "\n")
            session_file.write("NumPy version: " + np.version.version + "\n")
            session_file.write("Python version: " + sys.version + "\n")

    @staticmethod
    def load_model(learner: Learner, file_name: Optional[str] = None) -> None:
        if not file_name:
            file_name = "saved_model.pth"

        TorchHelper.create_model(learner)
        learner.model.load_state_dict(torch.load(learner.output_dir +
                                                 file_name))

    @staticmethod
    def get_num_params(learner: Learner) -> ModelSize:
        if learner.model is None:
            learner.create_model()
        num_trainable_params: int = sum(param.numel()
                                        for param in learner.model.parameters()
                                        if param.requires_grad)
        num_all_params: int = sum(param.numel()
                                  for param in learner.model.parameters())
        return ModelSize(num_trainable_params,
                         num_all_params - num_trainable_params)

    @staticmethod
    def get_optimizer(optimizer_hyperparameters, model_parameters):
        if "optimizer" in optimizer_hyperparameters:
            optimizer = \
                optimizer_hyperparameters["optimizer"].lower().strip()

            if "learning_rate" in optimizer_hyperparameters:
                learning_rate = float(
                    optimizer_hyperparameters["learning_rate"].strip())
            else:
                learning_rate = 0.001

            if "rho" in optimizer_hyperparameters:
                rho = float(
                    optimizer_hyperparameters["rho"].strip())
            else:
                rho = 0.9

            if "eps" in optimizer_hyperparameters:
                eps = float(
                    optimizer_hyperparameters["eps"].strip())
            else:
                eps = 1e-08

            if "weight_decay" in optimizer_hyperparameters:
                weight_decay = float(
                    optimizer_hyperparameters["weight_decay"].strip())
            else:
                weight_decay = 0.0

            if "momentum" in optimizer_hyperparameters:
                momentum = float(
                    optimizer_hyperparameters["momentum"].strip())
            else:
                momentum = 0.0

            if "lr_decay" in optimizer_hyperparameters:
                lr_decay = float(
                    optimizer_hyperparameters["lr_decay"].strip())
            else:
                lr_decay = 0.0

            if "initial_accumulator_value" in optimizer_hyperparameters:
                initial_accumulator_value = float(
                    optimizer_hyperparameters["initial_accumulator_value"].strip())
            else:
                initial_accumulator_value = 0.0

            if "betas" in optimizer_hyperparameters:
                betas = literal_eval(
                    optimizer_hyperparameters["betas"].strip())
            else:
                betas = (0.9, 0.999)

            if "amsgrad" in optimizer_hyperparameters:
                amsgrad = bool(strtobool(
                    optimizer_hyperparameters["amsgrad"].strip()))
            else:
                amsgrad = False

            if "lambd" in optimizer_hyperparameters:
                lambd = float(
                    optimizer_hyperparameters["lambd"].strip())
            else:
                lambd = 0.0001

            if "alpha" in optimizer_hyperparameters:
                alpha = float(
                    optimizer_hyperparameters["alpha"].strip())
            else:
                alpha = 0.75

            if "t0" in optimizer_hyperparameters:
                t0 = float(
                    optimizer_hyperparameters["t0"].strip())
            else:
                t0 = 1000000.0

            if "max_iter" in optimizer_hyperparameters:
                max_iter = int(
                    optimizer_hyperparameters["max_iter"].strip())
            else:
                max_iter = 20

            if "max_eval" in optimizer_hyperparameters:
                max_eval = int(
                    optimizer_hyperparameters["max_eval"].strip())
            else:
                max_eval = None

            if "tolerance_grad" in optimizer_hyperparameters:
                tolerance_grad = float(
                    optimizer_hyperparameters["tolerance_grad"].strip())
            else:
                tolerance_grad = 1e-07

            if "tolerance_change" in optimizer_hyperparameters:
                tolerance_change = float(
                    optimizer_hyperparameters["tolerance_change"].strip())
            else:
                tolerance_change = 1e-09

            if "history_size" in optimizer_hyperparameters:
                history_size = int(
                    optimizer_hyperparameters["history_size"].strip())
            else:
                history_size = 100

            if "line_search_fn" in optimizer_hyperparameters:
                line_search_fn = \
                    optimizer_hyperparameters["line_search_fn"].strip()
            else:
                line_search_fn = None

            if "centered" in optimizer_hyperparameters:
                centered = bool(strtobool(
                    optimizer_hyperparameters["centered"].strip()))
            else:
                centered = False

            if "etas" in optimizer_hyperparameters:
                etas = literal_eval(optimizer_hyperparameters["etas"].strip())
            else:
                etas = (0.5, 1.2)

            if "step_sizes" in optimizer_hyperparameters:
                step_sizes = literal_eval(
                    optimizer_hyperparameters["step_sizes"].strip())
            else:
                step_sizes = (1e-06, 50)

            if "dampening" in optimizer_hyperparameters:
                dampening = float(
                    optimizer_hyperparameters["dampening"].strip())
            else:
                dampening = 0.0

            if "nesterov" in optimizer_hyperparameters:
                nesterov = bool(strtobool(
                    optimizer_hyperparameters["nesterov"].strip()))
            else:
                nesterov = False

            if optimizer == "adadelta":
                if "eps" not in optimizer_hyperparameters:
                    eps = 1e-06
                return torch.optim.Adadelta(
                    model_parameters, lr=learning_rate, rho=rho, eps=eps,
                    weight_decay=weight_decay)
            elif optimizer == "adagrad":
                if "learning_rate" not in optimizer_hyperparameters:
                    learning_rate = 0.01
                if "eps" not in optimizer_hyperparameters:
                    eps = 1e-10

                return torch.optim.Adagrad(
                    model_parameters, lr=learning_rate, lr_decay=lr_decay,
                    weight_decay=weight_decay,
                    initial_accumulator_value=initial_accumulator_value,
                    eps=eps)
            elif optimizer == "adam":
                return torch.optim.Adam(
                    model_parameters, lr=learning_rate, betas=betas,
                    eps=eps, weight_decay=weight_decay, amsgrad=amsgrad)
            elif optimizer == "adamw":
                if "weight_decay" not in optimizer_hyperparameters:
                    weight_decay = 0.01

                return torch.optim.AdamW(
                    model_parameters, lr=learning_rate, betas=betas, eps=eps,
                    weight_decay=weight_decay, amsgrad=amsgrad)
            elif optimizer == "sparseadam":
                return torch.optim.SparseAdam(
                    model_parameters, lr=learning_rate, betas=betas,
                    eps=eps)
            elif optimizer == "adamax":
                if "learning_rate" not in optimizer_hyperparameters:
                    learning_rate = 0.002

                return torch.optim.Adamax(
                    model_parameters, lr=learning_rate, betas=betas, eps=eps,
                    weight_decay=weight_decay)
            elif optimizer == "asgd":
                if "learning_rate" not in optimizer_hyperparameters:
                    learning_rate = 0.01

                return torch.optim.ASGD(
                    model_parameters, lr=learning_rate, lambd=lambd,
                    alpha=alpha, t0=t0, weight_decay=weight_decay)
            elif optimizer == "lbfgs":
                if "learning_rate" not in optimizer_hyperparameters:
                    learning_rate = 1.0

                return torch.optim.LBFGS(
                    model_parameters, lr=learning_rate, max_iter=max_iter,
                    max_eval=max_eval, tolerance_grad=tolerance_grad,
                    tolerance_change=tolerance_change,
                    history_size=history_size, line_search_fn=line_search_fn)
            elif optimizer == "rmsprop":
                if "learning_rate" not in optimizer_hyperparameters:
                    learning_rate = 0.01
                if "alpha" not in optimizer_hyperparameters:
                    alpha = 0.99

                return torch.optim.RMSprop(
                    model_parameters, lr=learning_rate, alpha=alpha, eps=eps,
                    weight_decay=weight_decay, momentum=momentum,
                    centered=centered)
            elif optimizer == "rprop":
                if "learning_rate" not in optimizer_hyperparameters:
                    learning_rate = 0.01

                return torch.optim.Rprop(
                    model_parameters, lr=learning_rate, etas=etas,
                    step_sizes=step_sizes)
            elif optimizer == "rprop":
                if "learning_rate" not in optimizer_hyperparameters:
                    learning_rate = 0.01

                return torch.optim.Rprop(
                    model_parameters, lr=learning_rate, etas=etas,
                    step_sizes=step_sizes)
            elif optimizer == "sgd":
                return torch.optim.SGD(
                    model_parameters, lr=learning_rate, momentum=momentum,
                    dampening=dampening, weight_decay=weight_decay,
                    nesterov=nesterov)
            else:
                raise Exception("unknown optimizer specified: " + optimizer)
        else:
            raise Exception("no optimizer specified")

    @staticmethod
    def get_loss(loss_hyperparameters):
        if "loss" in loss_hyperparameters:
            loss = loss_hyperparameters["loss"].lower().replace(
                "_", "").strip()
            if loss == "crossentropyloss":
                return torch.nn.CrossEntropyLoss()
            elif loss == "nllloss":
                return torch.nn.NLLLoss()
            elif loss == "bceloss":
                return torch.nn.BCELoss()
            elif loss == "bcewithlogitsloss":
                return torch.nn.BCEWithLogitsLoss()
            elif loss == "l1loss":
                return torch.nn.L1Loss()
            elif loss == "mseloss":
                return torch.nn.MSELoss()
            elif loss == "smoothl1loss":
                return torch.nn.SmoothL1Loss()
            elif loss == "kldivloss":
                return torch.nn.KLDivLoss()
            elif loss == "marginrankingloss":
                return torch.nn.MarginRankingLoss()
            elif loss == "hingeembeddingloss":
                return torch.nn.HingeEmbeddingLoss()
            elif loss == "cosineembeddingloss":
                return torch.nn.CosineEmbeddingLoss()
            else:
                raise Exception("unknown loss specified: " + loss)
        else:
            raise Exception("no loss specified")

    @staticmethod
    def get_metrics(learner: Learner,
                    output_layer_activation_function: Optional[str] = None):
        logger = logging.getLogger(__name__)

        def thresholded_output_transform(output):
            y_hat, y = output
            y_hat = torch.round(y_hat)
            return y_hat, y

        def softmax_thresholded_output_transform(output):
            y_hat, y = output
            y_hat = torch.nn.functional.softmax(y_hat, dim=1)
            y_hat = torch.round(y_hat)
            return y_hat, y

        def sigmoid_thresholded_output_transform(output):
            y_hat, y = output
            y_hat = torch.sigmoid(y_hat)
            y_hat = torch.round(y_hat)
            return y_hat, y

        is_multilabel = learner.definition.task == c.TaskType.MULTI_LABEL_CLASSIFICATION
        metrics_dict = dict()
        for metric in learner.metrics:
            metric = metric.lower().strip()
            if metric == "loss":
                metrics_dict[metric] = Loss(learner.criterion)
            elif metric == "accuracy":
                if is_multilabel:
                    if output_layer_activation_function is None:
                        metrics_dict[metric] = Accuracy(
                            thresholded_output_transform,
                            is_multilabel=is_multilabel)
                    elif output_layer_activation_function == "softmax":
                        metrics_dict[metric] = Accuracy(
                            softmax_thresholded_output_transform,
                            is_multilabel=is_multilabel)
                    elif output_layer_activation_function == "sigmoid":
                        metrics_dict[metric] = Accuracy(
                            sigmoid_thresholded_output_transform,
                            is_multilabel=is_multilabel)
                else:
                    metrics_dict[metric] = Accuracy(
                        is_multilabel=is_multilabel)
            else:
                logger.warning("unknown metric: %s", metric)
        return metrics_dict
