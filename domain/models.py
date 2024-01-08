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

