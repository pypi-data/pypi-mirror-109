"""
Creates ROC curves of different models

Classes:
    - :class:`~seqgra.comparator.roccomparator.ROCComparator`: creates ROC curves from various grammars and architectures
"""
from typing import List, Optional
import os

import matplotlib.pyplot as plt
import pandas as pd
from sklearn.metrics import roc_curve, auc

import seqgra.constants as c
from seqgra.comparator import Comparator


class ROCComparator(Comparator):
    def __init__(self, analysis_id: str, output_dir: str,
                 model_labels: Optional[List[str]] = None,
                 silent: bool = False) -> None:
        super().__init__(c.ComparatorID.ROC, "ROC curve", analysis_id,
                         output_dir, model_labels, silent)

    def compare_models(self, grammar_ids: Optional[List[str]] = None,
                       model_ids: Optional[List[str]] = None,
                       set_names: List[str] = None) -> None:
        if not set_names:
            set_names = ["test"]

        fpr: List[List[float]] = list()
        tpr: List[List[float]] = list()
        roc_auc: List[float] = list()
        valid_labels: List[str] = list()
        if len(grammar_ids) == 1 and len(set_names) == 1:
            for model_id in model_ids:
                predict_file_name: str = self.evaluation_dir + \
                    grammar_ids[0] + "/" + \
                    model_id + "/" + c.EvaluatorID.PREDICT + \
                    "/" + set_names[0] + "-y-hat.txt"
                if os.path.isfile(predict_file_name):
                    df = pd.read_csv(predict_file_name, sep="\t")
                    num_labels: int = int(len(df.columns) / 2)
                    y_df = df.iloc[:, 0:num_labels]
                    y_hat_df = df.iloc[:, num_labels:len(df.columns)]

                    current_fpr, current_tpr, current_auc = self.create_single_roc_curve(
                        y_df.values, y_hat_df.values)
                    fpr.append(current_fpr)
                    tpr.append(current_tpr)
                    roc_auc.append(current_auc)
                    valid_labels.append(model_id)
                else:
                    self.logger.warning("file does not exist: %s",
                                        predict_file_name)
        elif len(model_ids) == 1 and len(set_names) == 1:
            for grammar_id in grammar_ids:
                predict_file_name: str = self.evaluation_dir + \
                    grammar_id + "/" + \
                    model_ids[0] + "/" + c.EvaluatorID.PREDICT + \
                    "/" + set_names[0] + "-y-hat.txt"
                if os.path.isfile(predict_file_name):
                    df = pd.read_csv(predict_file_name, sep="\t")
                    num_labels: int = int(len(df.columns) / 2)
                    y_df = df.iloc[:, 0:num_labels]
                    y_hat_df = df.iloc[:, num_labels:len(df.columns)]

                    current_fpr, current_tpr, current_auc = self.create_single_roc_curve(
                        y_df.values, y_hat_df.values)
                    fpr.append(current_fpr)
                    tpr.append(current_tpr)
                    roc_auc.append(current_auc)
                    valid_labels.append(grammar_id)
                else:
                    self.logger.warning("file does not exist: %s",
                                        predict_file_name)
        else:
            # TODO
            pass

        if not self.model_labels or len(self.model_labels) != len(valid_labels):
            self.model_labels = valid_labels

        self.create_roc_curve(fpr, tpr, roc_auc, self.model_labels,
                              self.output_dir + set_names[0] +
                              "-roc-curve.pdf")

    def create_single_roc_curve(self, y_true, y_hat) -> None:
        """Create ROC curve.

        Plots ROC curves for each class label, including micro-average and
        macro-average. Saves plot as PDF in `file_name`.

        Arguments:
            y_true (array): TODO ; shape = [n_samples, n_classes]
            y_hat (array): TODO ; shape = [n_samples, n_classes]
        """
        # Compute micro-average ROC curve and ROC area
        fpr, tpr, _ = roc_curve(
            y_true.ravel(), y_hat.ravel())
        roc_auc = auc(fpr, tpr)

        return fpr, tpr, roc_auc

    def create_roc_curve(self, fpr: List[List[float]], tpr: List[List[float]],
                         roc_auc: List[float], model_labels: List[str],
                         file_name: str) -> None:
        n_lines = len(model_labels)
        # Plot all ROC curves
        plt.figure(figsize=(7, 7))
        lines = []
        labels = []

        for i in range(n_lines):
            line, = plt.plot(fpr[i], tpr[i], linewidth=2)
            lines.append(line)
            labels.append(
                "{0} (area = {1:0.2f})"
                "".format(model_labels[i], roc_auc[i]))

        plt.plot([0, 1], [0, 1], "k--", linewidth=2)
        plt.xlim([0.0, 1.0])
        plt.ylim([0.0, 1.05])
        plt.xlabel("False Positive Rate")
        plt.ylabel("True Positive Rate")
        plt.title("ROC curve")
        plt.legend(lines, labels, bbox_to_anchor=(1.04, 1),
                   loc="upper left", prop=dict(size=14))
        plt.savefig(file_name, bbox_inches="tight")
