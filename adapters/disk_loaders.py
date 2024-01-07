import os
import abc
import json

from domain import models


class AbstractDiskLoader(abc.ABC):

    def __init__(self, folder: str):
        self.folder = folder

    def generate_path_to_file(self, file_name: str) -> str:
        return rf"{os.getcwd()}\{self.folder}\{file_name}"

    @abc.abstractmethod
    def load(self, **kwargs) -> None:
        raise NotImplementedError


class DatasetLoaderAdapter(AbstractDiskLoader):

    def load(self, file: str, value_name: str) ->  models.Dataset:
        with open(self.generate_path_to_file(file), encoding="utf-8") as f:
            dataset = json.load(f)
            return models.Dataset(
                name=file.split(".")[0],
                labels=[item["label"] for item in dataset],
                values=[item[value_name] for item in dataset]
            )
