import inspect

from typing import Dict, List, Callable, Type

from domain import commands
from services import message_bus, trainers, http_service, model_store, classifiers


class Injector:

    def __init__(
        self,
        command_handlers: Dict[Type[commands.BaseCommand], Callable]
    ):
        self.command_handlers = command_handlers
        self.dependencies = {
            "trainer": trainers.TrainerService,
            "global_model_store": model_store.GlobalClassificationModels(),
            "http_sender": http_service.HttpService(),
            "classifier_service": classifiers.ClassifierService
        }

    def _inject_dependencies(self, handler_func: Callable) -> Callable:
        """
        Injects default dependency values into the handler function.

        :param handler_func:
        :return: Callable
        """
        inspector = inspect.signature(handler_func)
        function_dependencies = {
            name: dep
            for name, dep in self.dependencies.items()
            if name in inspector.parameters
        }

        return lambda item: handler_func(item, **function_dependencies)

    def inject_handlers(self) -> message_bus.MessageBus:
        """
        Injects the handlers using the poor man's injection method.

        :return: MessageBus
        """
        return message_bus.MessageBus(command_handlers={
            item_type: self._inject_dependencies(handler_func)
            for item_type, handler_func in self.command_handlers.items()
        })
