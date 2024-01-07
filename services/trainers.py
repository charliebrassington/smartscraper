from typing import List, Any, Dict

from adapters import disk_loaders
from domain import models

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import LabelEncoder


class TrainerService:

    def __init__(self, name: str) -> None:
        disk_loader = disk_loaders.DatasetLoaderAdapter(folder="datasets")
        self.dataset = disk_loader.load(file=f"{name}_dataset.json", value_name=name)
        self._preprocessing_methods: Dict[str, object] = {
            "values": CountVectorizer(),
            "labels": LabelEncoder()
        }

    def process_dataset(self) ->  List[Any]:
        return [
            method.fit_transform(getattr(self.dataset, attribute))
            for attribute, method in self._preprocessing_methods.items()
        ]

    def train(self) -> models.TrainedModel:
        model = MLPClassifier(hidden_layer_sizes=(100, 50), max_iter=5000)
        model.fit(*self.process_dataset())

        return models.TrainedModel(
            model=model,
            count_vectorizer=self._preprocessing_methods["values"],
            label_encoder=self._preprocessing_methods["labels"]
        )
