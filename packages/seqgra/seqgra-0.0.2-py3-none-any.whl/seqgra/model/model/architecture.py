"""
MIT - CSAIL - Gifford Lab - seqgra

Architecture class definition, markup language agnostic

@author: Konstantin Krismer
"""
from typing import Dict, List, Optional

from seqgra.model.model import Operation


class Architecture:
    def __init__(self, operations: Optional[List[Operation]] = None,
                 hyperparameters: Optional[Dict[str, str]] = None,
                 external_model_path: Optional[str] = None,
                 external_model_format: Optional[str] = None,
                 external_model_class_name: Optional[str] = None) -> None:
        if (operations is not None or hyperparameters is not None) and \
            (external_model_path is not None or
                external_model_format is not None or
             external_model_class_name is not None):
            raise Exception("cannot both specify operations / "
                            "hyperparameters and external model")
        self.operations: Optional[List[Operation]] = operations
        self.hyperparameters: Optional[Dict[str, str]] = hyperparameters
        self.external_model_path: Optional[str] = external_model_path
        self.external_model_format: Optional[str] = external_model_format
        self.external_model_class_name: Optional[str] = \
            external_model_class_name

    def __str__(self):
        str_rep = ["Architecture:\n"]

        if self.operations is not None and len(self.operations) > 0:
            str_rep += ["\tSequential:\n"]
            operators_string: List[str] = [str(operation)
                                           for operation in self.operations]
            operators_str_rep = "".join(operators_string)
            str_rep += ["\t\t" + s + "\n"
                        for s in operators_str_rep.splitlines()]

        if self.hyperparameters is not None and len(self.hyperparameters) > 0:
            str_rep += ["\tHyperparameters:\n", "\t\t",
                        str(self.hyperparameters)]

        if self.external_model_path is not None:
            str_rep += ["\tExternal model path:\n", "\t\t",
                        self.external_model_path]
        if self.external_model_path is not None:
            str_rep += ["\tExternal model format:\n", "\t\t",
                        self.external_model_format]
        if self.external_model_class_name is not None:
            str_rep += ["\tExternal model class name:\n", "\t\t",
                        self.external_model_class_name]

        return "".join(str_rep)
