import abc
import typing
import json
import collections
import bs4

from services import classifiers, flattener
from domain import models


class AbstractParserService(abc.ABC):

    def __init__(self, classifier: classifiers.AbstractClassifier):
        self.classifier = classifier

    @abc.abstractmethod
    def gather_tasks(self, data: typing.Any) -> typing.List[str]:
        raise NotImplementedError

    def parse(self, data: typing.Any) -> typing.List[models.ResultCategory]:
        tasks = self.gather_tasks(data=data)
        return self.classifier.classify_tasks(task_list=tasks)


class HtmlParser(AbstractParserService):

    def _parse_value(self, value: typing.Union[str, list]) -> str:
        return "-".join(value) if isinstance(value, list) else value

    def _build_html_element(self, element):
        string_contents = "".join(content for content in element.contents if not isinstance(content, bs4.element.Tag))
        string_attrs = " " + " ".join(f'{name}="{self._parse_value(value)}"' for name, value in element.attrs.items()) if element.attrs else ""
        return f"<{element.name}{string_attrs}>{''.join(string_contents)}</{element.name}>"

    def gather_tasks(self, data: typing.Any) -> typing.List[str]:
        tasks = [
            self._build_html_element(element=element)
            for tag_name in list({tag.name for tag in data.find_all()})
            for element in data.find_all(tag_name)
        ]

        return [task for task in tasks if not task.startswith(("<style", "<path"))]


class JsonParser(AbstractParserService):

    def gather_tasks(self, data: typing.Any) -> typing.List[str]:
        parsed_json_data = self._parse_raw_data(data=str(data))
        json_flattener = flattener.DataFlattenerService()
        return json_flattener.get_flattened_data(parsed_json=parsed_json_data)

    def _parse_raw_data(self, data: str) -> typing.Union[list, dict]:
        removed_left_side = "{" + '{'.join(data.split("{")[1:])
        removed_right_side = "}".join(removed_left_side.split("}")[:-1]) + "}"
        return json.loads(removed_right_side)


name_to_parser = {
    "html": HtmlParser,
    "json": JsonParser
}
