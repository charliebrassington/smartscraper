import typing
import bs4
import collections

from domain import commands, models
from services import (
    parsers,
    classifiers,
    http_service,
    trainers,
    model_store
)


def _handle_classifying(
    name: str,
    data: typing.Any,
    global_model_store: model_store.GlobalClassificationModels,
    classifier_service: typing.Type[classifiers.ClassifierService]
) -> typing.List[models.ResultCategory]:
    trained_model = global_model_store.get_trained_model(name=name)
    if trained_model is None:
        return []

    classifier = classifier_service(trained_model=trained_model)
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
    trainer: typing.Type[trainers.TrainerService],
    global_model_store: model_store.GlobalClassificationModels
) -> None:
    trainer_object = trainer(name=cmd.model_name)
    trained_model = trainer_object.train(training_loops=cmd.training_iterations)

    global_model_store.add_trained_model(name=cmd.model_name, trained_model=trained_model)


def scrape_url_handler(
    cmd: commands.ScrapeUrl,
    http_sender: http_service.HttpService,
    global_model_store: model_store.GlobalClassificationModels,
    classifier_service: typing.Type[classifiers.ClassifierService]
) -> typing.Dict[str, typing.List[str]]:
    dp_kwargs = {
        "global_model_store": global_model_store,
        "classifier_service": classifier_service
    }

    soup = http_sender.get_parsed_html(url=cmd.url)
    results = _handle_classifying(name="html", data=soup, **dp_kwargs)

    json_classified_data = [
        value
        for result in results
        if result.name == "json"
        for value in result.classified_values
    ]

    results.extend(
        result
        for data in json_classified_data
        for result in _handle_classifying(name="json", data=data, **dp_kwargs)
    )

    return _parse_data(results)


command_handlers = {
    commands.TrainModel: train_model_handler,
    commands.ScrapeUrl: scrape_url_handler
}
