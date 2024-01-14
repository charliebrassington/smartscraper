import typing
import bs4

from domain import models
from services import classifiers, parsers


class FakeClassifier(classifiers.AbstractClassifier):

    def classify_text(self, unclassified_text: str) -> None:
        pass

    def classify_tasks(self, task_list: typing.List[str]) -> typing.List[models.ResultCategory]:
        pass


def create_soup(html):
    return bs4.BeautifulSoup(html, features="lxml")


def test_parser_parses_html():
    html_parser = parsers.HtmlParser(classifier=FakeClassifier())
    tasks = html_parser.gather_tasks(data=create_soup('<div>div-value <p class="bob"></p></div>'))
    expected_tasks = ['<html></html>', '<body></body>', '<p class="bob"></p>', '<div>div-value </div>']
    assert tasks[0] in expected_tasks
    assert tasks[3] in expected_tasks


test_parser_parses_html()
