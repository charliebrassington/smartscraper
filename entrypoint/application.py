import flask
import json

from domain import commands
from services.message_bus import MessageBus


flask_app = flask.Flask(__name__)


message_bus = MessageBus()


@flask_app.route("/api/model/train", methods=["POST"])
def train_model():
    body = flask.request.get_json()
    if "name" not in body:
        return flask.jsonify({"error": "the model name is not in the body"})

    cmd = commands.TrainModel(
        model_name=body["name"],
        training_iterations=body.get("training_iterations", 500)
    )

    message_bus.run_command_handler(cmd=cmd)

    return flask.jsonify({"success": "the model has been trained"})


@flask_app.route("/api/scrape", methods=["POST"])
def scrape_url():
    body = flask.request.get_json()
    if "url" not in body:
        return flask.jsonify({"error": "the url is not in the body"})

    cmd = commands.ScrapeUrl(url=body["url"])
    result = message_bus.run_command_handler(cmd=cmd)

    return flask.jsonify({"success": "successfully scraped the url", "result": result})
