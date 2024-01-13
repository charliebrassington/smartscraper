from dataclasses import dataclass
from typing import (
    Any,
    Type,
    Dict,
    Callable
)

from domain import commands
from services import trainers, http_service, model_store, classifiers, handlers


class MessageBus:

    def __init__(
        self,
        http_sender: http_service.HttpService = http_service.HttpService(),
        global_model_store: model_store.GlobalClassificationModels = model_store.GlobalClassificationModels(),
        classifier_service: Type[classifiers.ClassifierService] = classifiers.ClassifierService,
        trainer: Type[trainers.TrainerService] = trainers.TrainerService
    ):
        self._cmd_lookup: Dict[Any, Callable] = {
            commands.ScrapeUrl: lambda cmd: handlers.scrape_url_handler(cmd, http_sender, global_model_store, classifier_service),
            commands.TrainModel: lambda cmd: handlers.train_model_handler(cmd, trainer, global_model_store)
        }

    def run_command_handler(self, cmd: commands.BaseCommand) -> Any:
        """
        Finds the handler paired to the command passed in then runs and returns the handlers result.

        :param cmd: type of base command
        :return: Any
        """
        return self._cmd_lookup[type(cmd)](cmd)
