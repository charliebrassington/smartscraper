from dataclasses import dataclass

from domain import models

class BaseCommand:
    pass


@dataclass
class ScrapeUrl(BaseCommand):
    url: str


@dataclass
class TrainModel(BaseCommand):
    model_name: str
