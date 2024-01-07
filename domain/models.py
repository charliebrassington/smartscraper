from dataclasses import dataclass
from typing import List, Dict

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import LabelEncoder


@dataclass
class Dataset:
    name: str
    labels: List[str]
    values: List[str]


@dataclass
class TrainedModel:
    model: MLPClassifier
    label_encoder: LabelEncoder
    count_vectorizer: CountVectorizer


@dataclass
class ResultCategory:
    name: str
    classified_values: List[str]


class GlobalClassificationModels:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(GlobalClassificationModels, cls).__new__(cls)
            cls._instance._models = {}

        return cls._instance

    def add_trained_model(self, name: str, trained_model: TrainedModel) -> None:
        self._models[name] = trained_model

    def get_trained_model(self, name: str) -> TrainedModel:
        return self._models[name]
