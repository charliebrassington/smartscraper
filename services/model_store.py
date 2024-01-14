from domain import models


class GlobalClassificationModels:

    def __init__(self):
        self._models = {}

    def add_trained_model(self, name: str, trained_model: models.TrainedModel) -> None:
        self._models[name] = trained_model

    def get_trained_model(self, name: str) -> models.TrainedModel | None:
        return self._models.get(name)
