from flask import Flask, request, Response, abort
import cherrypy
import json
import os
from jinja2 import Template
import uuid
import datetime
import requests
import sys
import logging

app = Flask(__name__)

logger = logging.getLogger()
format_string = '[%(asctime)s] %(levelname)s %(message)s'
log_handler = logging.StreamHandler()
log_handler.setFormatter(logging.Formatter(format_string))
logger.addHandler(log_handler)
logger.setLevel(logging.INFO)

config = json.loads(os.getenv("config", "{}"))
if not config or type(config) is not dict:
    logger.error("Config missing or invalid!")
    sys.exit(1)

required_config_keys = ["template", "endpoint_url", "batch_payload_key"]
for key in required_config_keys:
    if key not in config:
        logger.error(f"Missing required config key '{key}'!")
        sys.exit(1)


@app.route('/receiver', methods=['POST'])
def receiver():
    entities = request.get_json()
    if not isinstance(entities, list):
        entities = [entities]

    message_size = len(entities)
    if message_size > 9999:  # MDE message limitation
        logger.error("Batch exceeds allowed limit (9999).")
        return abort(400)

    logger.info(f"Constructing message with {message_size} entities")
    message = construct_message(entities)

    response = requests.post(config["endpoint_url"], json=message, headers=config.get("headers"))
    if response.status_code == requests.codes.ok:
        logger.info(f"Successfully sent {message_size} entities to MDE endpoint")
        return Response(200)

    logger.error(f"Failed to send batch to MDE/Elhub. Error code {response.status_code}. "
                 f"Received the following error message from endpoint: {response.text}")

    return Response("Failed to send batch to MDE/Elhub", 500)


def construct_message(entities):

    template = Template(config["template"])
    uuid1 = uuid.uuid4().hex
    now = datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc).isoformat()
    string_output = template.render(uuid=uuid1, now=now)
    dict_output = json.loads(string_output)

    payload_key = config["batch_payload_key"]

    for entity in entities:
        strip_system_attributes(entity)

    dict_output["Payload"][payload_key] = entities

    return dict_output


def strip_system_attributes(entity):
    for key in list(entity.keys()):
        if key.startswith("_"):
            del entity[key]


if __name__ == '__main__':
    cherrypy.tree.graft(app, '/')

    # Set the configuration of the web server to production mode
    cherrypy.config.update({
        'environment': 'production',
        'engine.autoreload_on': False,
        'log.screen': False,
        'server.socket_port': 5001,
        'server.socket_host': '0.0.0.0'
    })

    # Start the CherryPy WSGI web server
    cherrypy.engine.start()
    cherrypy.engine.block()
