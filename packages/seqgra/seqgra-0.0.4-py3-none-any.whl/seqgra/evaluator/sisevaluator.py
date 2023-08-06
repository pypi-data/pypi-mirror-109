"""
MIT - CSAIL - Gifford Lab - seqgra

- abstract base class for all evaluators

@author: Konstantin Krismer
"""
from __future__ import annotations

from typing import Any, List, Optional

import numpy as np
import pandas as pd

import seqgra.constants as c
from seqgra.evaluator import FeatureImportanceEvaluator
from seqgra.evaluator import sis
from seqgra.learner import Learner


class SISEvaluator(FeatureImportanceEvaluator):
    def __init__(self, learner: Learner, output_dir: str,
                 predict_threshold: Optional[float] = None,
                 silent: bool = False) -> None:
        super().__init__(
            c.EvaluatorID.SIS, "Sufficient Input Subsets", learner, output_dir,
            supported_tasks=[c.TaskType.MULTI_CLASS_CLASSIFICATION,
                             c.TaskType.MULTI_LABEL_CLASSIFICATION],
            silent=silent)

        if predict_threshold:
            self.predict_threshold = predict_threshold
        else:
            self.predict_threshold = 0.5

    def _evaluate_model(self, x: List[str], y: List[str],
                        annotations: List[str]) -> Any:
        x_column: List[str] = list()
        y_column: List[str] = list()
        label_column: List[str] = list()
        annotations_column: List[str] = list()
        sis_collapsed_column: List[str] = list()
        sis_separated_column: List[str] = list()

        for selected_label in self.learner.get_label_set(y):
            # select x, y, annotations of examples with label
            selected_x, selected_y, selected_annotations = \
                self._subset_by_label(x, y, annotations, {selected_label})

            model_label_index: int = self.learner.definition.labels.index(
                selected_label)

            sis_results: List[List[str]] = self.find_sis(
                selected_x, model_label_index)
            sis_collapsed: List[str] = [self.__collapse_sis(sis_col)
                                        for sis_col in sis_results]
            sis_separated: List[str] = [";".join(sis_col)
                                        for sis_col in sis_results]

            x_column += selected_x
            y_column += selected_y
            label_column += [selected_label] * len(selected_x)
            annotations_column += selected_annotations
            sis_collapsed_column += sis_collapsed
            sis_separated_column += sis_separated

        return pd.DataFrame({"x": x_column,
                             "y": y_column,
                             "label": label_column,
                             "annotation": annotations_column,
                             "sis_collapsed": sis_collapsed_column,
                             "sis_separated": sis_separated_column})

    def _save_results(self, results, set_name: str = "test",
                      suppress_plots: bool = False) -> None:
        if results is None:
            results = pd.DataFrame([], columns=["x", "y", "label",
                                                "annotation",
                                                "sis_collapsed",
                                                "sis_separated"])

        results.to_csv(self.output_dir + set_name + "-df.txt", sep="\t",
                       index=False)

    def __get_agreement_group(self, annotation_position: str,
                              sis_position: str) -> str:
        masked_letter: str = self.__get_masked_letter()

        if annotation_position == c.PositionType.GRAMMAR:
            if sis_position == masked_letter:
                return "FN"
            else:
                return "TP"
        else:
            if sis_position == masked_letter:
                return "TN"
            else:
                return "FP"

    def _convert_to_data_frame(self, results) -> pd.DataFrame:
        """Takes SIS evaluator-specific results and turns them into a pandas
        data frame.

        The data frame has the following columns:
            - example_column (int): example index
            - position (int): position within example (one-based)
            - group (str): group label, one of the following:
                - "TP": grammar position, important for model prediction
                - "FN": grammar position, not important for model prediction,
                - "FP": background position, important for model prediction,
                - "TN": background position, not important for model prediction
            - label (str): label of example, e.g., "cell type 1"
        """
        example_column: List[int] = list()
        position_column: List[int] = list()
        group_column: List[str] = list()
        label_column: List[str] = list()

        for example_id, row in enumerate(results.itertuples(), 1):
            example_column += [example_id] * len(row.annotation)
            position_column += list(range(1, len(row.annotation) + 1))
            if row.sis_collapsed:
                group_column += [self.__get_agreement_group(char, row.sis_collapsed[i])
                                 for i, char in enumerate(row.annotation)]
            else:
                group_column += [self.__get_agreement_group(char, self.__get_masked_letter())
                                 for i, char in enumerate(row.annotation)]
            label_column += [row.label] * len(row.annotation)

        df = pd.DataFrame({"example": example_column,
                           "position": position_column,
                           "group": group_column,
                           "label": label_column})

        return df

    def _visualize_grammar_agreement(self, results,
                                     set_name: str = "test") -> None:
        df: pd.DataFrame = self._convert_to_data_frame(results)
        if len(df.index) > 0:
            df.to_csv(self.output_dir + set_name +
                      "-grammar-agreement-thresholded-df.txt",
                      sep="\t", index=False)

            pdf_file_name: str = set_name + "-grammar-agreement-thresholded.pdf"
            df: pd.DataFrame = self._prepare_r_data_frame(df)
            caption: str = "prediction threshold for SIS: " + \
                str(self.predict_threshold) + \
                ":NL:(model prediction of true class exceeds this threshold with grammar positions alone)"
            self._execute_plotting_command(df, set_name, pdf_file_name,
                                           self.evaluator_name, caption)

    def find_sis(self, x: List[str], label_index: int) -> List[List[str]]:
        encoded_x = self.learner.encode_x(x)

        def sis_predict(x):
            return np.array(self.learner.predict(
                x=x, encode=False))[:, label_index]

        input_shape: int = encoded_x[0].shape
        if self.learner.definition.library == c.LibraryType.TENSORFLOW:
            broadcast_axis: int = 1
        elif self.learner.definition.library == c.LibraryType.TORCH:
            broadcast_axis: int = 0
        elif self.learner.definition.library == c.LibraryType.BAYES_OPTIMAL_CLASSIFIER:
            broadcast_axis: int = 1
        else:
            raise Exception("unknown library type")

        fully_masked_input = np.ones(input_shape) * 0.25
        initial_mask = sis.make_empty_boolean_mask_broadcast_over_axis(
            input_shape, broadcast_axis)

        return [self.__produce_masked_inputs(
            encoded_x[i], sis_predict,
            fully_masked_input, initial_mask)
            for i in range(len(encoded_x))]

    def __get_masked_letter(self) -> str:
        if self.learner.definition.sequence_space == c.SequenceSpaceType.DNA:
            return c.PositionType.DNA_MASKED
        else:
            return c.PositionType.AA_MASKED

    def __collapse_sis(self, sis: List[str]) -> str:
        masked_letter: str = self.__get_masked_letter()

        if not sis:
            return ""
        elif len(sis) == 1:
            return sis[0]
        else:
            collapsed_sis: str = sis[0]
            sis.pop(0)
            for i, char in enumerate(collapsed_sis):
                if char == masked_letter:
                    for s in sis:
                        if s[i] != masked_letter:
                            collapsed_sis = collapsed_sis[:i] + \
                                s[i] + collapsed_sis[(i + 1):]
            return collapsed_sis

    def __produce_masked_inputs(self, x, sis_predict, fully_masked_input,
                                initial_mask) -> List[str]:
        collection = sis.sis_collection(sis_predict, self.predict_threshold, x,
                                        fully_masked_input,
                                        initial_mask=initial_mask)

        if len(collection) > 0:
            sis_masked_inputs = sis.produce_masked_inputs(
                x, fully_masked_input,
                [sr.mask for sr in collection])
            return self.learner.decode_x(sis_masked_inputs).tolist()
        else:
            return list()
