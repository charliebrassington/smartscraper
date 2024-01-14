import abc
import typing
import collections

from domain import models

from sklearn.neural_network import MLPClassifier


class AbstractClassifier(abc.ABC):

    @abc.abstractmethod
    def classify_text(self, unclassified_text: str) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def classify_tasks(self, task_list: typing.List[str]) -> typing.List[models.ResultCategory]:
        raise NotImplementedError


class ClassifierService(AbstractClassifier):

    def __init__(self, trained_model: models.TrainedModel):
        self.trained_model = trained_model

    def classify_text(self, unclassified_text: str) -> str | None:
        vectorized_text = self.trained_model.count_vectorizer.transform([unclassified_text])
        predicted_probability = self.trained_model.model.predict_proba(vectorized_text)[0]

        predicted_label_index = predicted_probability.argmax()
        probability = predicted_probability[predicted_label_index]

        if probability < 0.7:
            return None

        return self.trained_model.label_encoder.inverse_transform([predicted_label_index])[0]

    def classify_tasks(self, task_list: typing.List[str]) -> typing.List[models.ResultCategory]:
        results = collections.defaultdict(list)
        for task in task_list:
            label = self.classify_text(unclassified_text=task)
            if label is not None:
                results[label].append(task)

        return [
            models.ResultCategory(name=name, classified_values=values)
            for name, values in results.items()
            if name not in {"unknown", "unwanted"}
        ]
