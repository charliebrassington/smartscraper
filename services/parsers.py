import abc
import typing
import json
import collections

from services import classifiers, flattener
from domain import models


class AbstractParserService(abc.ABC):

    def __init__(self, classifier: classifiers.ClassifierService):
        self.classifier = classifier
        self.tasks = []

    @abc.abstractmethod
    def _guess_label(self, text: typing.Any) -> str | None:
        raise NotImplementedError

    @abc.abstractmethod
    def _gather_tasks(self, data: typing.Any) -> None:
        raise NotImplementedError

    def parse(self, data: typing.Any) -> typing.List[models.ResultCategory]:
        self._gather_tasks(data=data)
        results = collections.defaultdict(list)
        for task in self.tasks:
            label = self._guess_label(text=task)
            if label is not None:
                results[label].append(task)

        return [
            models.ResultCategory(name=name, classified_values=values)
            for name, values in results.items()
            if name not in {"unknown", "unwanted"}
        ]


class HtmlParser(AbstractParserService):

    def _guess_label(self, text: typing.Any) -> str | None:
        if text.name not in {"style", "path"}:
            return self.classifier.classify_text(unclassified_text=str(text))

        return None

    def _gather_tasks(self, data: typing.Any) -> None:
        self.tasks.extend(
            element
            for tag_name in list({tag.name for tag in data.find_all()})
            for element in data.find_all(tag_name)
            if not element.find_all(recursive=False)
        )


class JsonParser(AbstractParserService):

    def _guess_label(self, text: typing.Any) -> str | None:
        return self.classifier.classify_text(unclassified_text=text)

    def _gather_tasks(self, data: typing.Any) -> None:
        parsed_json_data = self._parse_raw_data(data=str(data))
        json_flattener = flattener.DataFlattenerService()
        self.tasks.extend(json_flattener.get_flattened_data(parsed_json=parsed_json_data))

    def _parse_raw_data(self, data: str) -> typing.Union[list, dict]:
        removed_left_side = "{" + '{'.join(data.split("{")[1:])
        removed_right_side = "}".join(removed_left_side.split("}")[:-1]) + "}"
        return json.loads(removed_right_side)


name_to_parser = {
    "html": HtmlParser,
    "json": JsonParser
}
