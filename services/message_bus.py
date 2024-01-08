from dataclasses import dataclass
from typing import (
    Any,
    Type,
    Dict,
    Callable
)

from domain import commands


class MessageBus:

    def __init__(
        self,
        command_handlers: Dict[Type[commands.BaseCommand], Callable],
    ):
        self._command_handlers = command_handlers

    def run_command_handler(self, cmd: commands.BaseCommand) -> Any:
        """
        Finds the handler paired to the command passed in then runs and returns the handlers result.

        :param cmd: type of base command
        :return: Any
        """
        return self._command_handlers[type(cmd)](cmd)
