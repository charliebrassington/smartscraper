import typing
import bs4
import collections

from domain import commands, models
from services import parsers, classifiers, http_service, trainers


def _handle_classifying(
    name: str,
    data: typing.Any
) -> typing.List[models.ResultCategory]:
    global_models = models.GlobalClassificationModels()
    trained_model = global_models.get_trained_model(name=name)

    classifier = classifiers.ClassifierService(trained_model=trained_model)
    parser = parsers.name_to_parser[name](classifier=classifier)

    return parser.parse(data=data)


def _parse_data(
    data_list: typing.List[models.ResultCategory]
) -> dict:
    results = collections.defaultdict(list)
    for data in data_list:
        results[data.name].extend(str(value) for value in data.classified_values)

    return dict(results)


def train_model_handler(
    cmd: commands.TrainModel,
    trainer: typing.Type[trainers.TrainerService]
) -> None:
    trainer_object = trainer(name=cmd.model_name)
    trained_model = trainer_object.train()

    global_models = models.GlobalClassificationModels()
    global_models.add_trained_model(name=cmd.model_name, trained_model=trained_model)


def scrape_url_handler(
    cmd: commands.ScrapeUrl
) -> typing.Dict[str, typing.List[str]]:

    http_sender = http_service.HttpService()
    soup = http_sender.get_parsed_html(url=cmd.url)

    results = _handle_classifying(name="html", data=soup)
    json_classified_data = [
        value
        for result in results
        if result.name == "json"
        for value in result.classified_values
    ]

    results.extend(
        result
        for data in json_classified_data
        for result in _handle_classifying(name="json", data=data)
    )

    return _parse_data(results)


command_handlers = {
    commands.TrainModel: train_model_handler,
    commands.ScrapeUrl: scrape_url_handler
}
