from flask import Flask, request, Response, abort
import cherrypy
import json
import os
from jinja2 import Template
import uuid
import datetime
from requests import request, codes
import sys

app = Flask(__name__)

config = os.getenv("config")
if not config or type(config) is not dict:
    app.logger.error("Config missing or invalid!")
    sys.exit(1)

required_config_keys = ["template", "endpoint_url", "batch_payload_key"]
for key in required_config_keys:
    if key not in config:
        app.logger.error(f"Missing required config key '{key}'!")
        sys.exit(1)


@app.route('/receiver', methods=['POST'])
def receiver():
    entities = request.get_json()
    if not isinstance(entities, list):
        entities = [entities]

    if len(entities) > 9999:  # MDE message limitation
        return abort(400)

    message = construct_message(entities)

    response = request.post(config["endpoint_url"], json=message)
    if response.status_code == codes.ok:
        return Response(200)

    return Response("Failed to send batch to MDE/Elhub", 500)


def construct_message(entities):

    template = Template(config["template"])
    uuid1 = uuid.uuid4().hex
    now = datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc).isoformat()
    string_output = template.render(uuid=uuid1, now=now, entities=entities)
    dict_output = json.loads(string_output)

    payload_key = config["batch_payload_key"]
    dict_output["Payload"][payload_key] = entities

    return dict_output


if __name__ == '__main__':
    cherrypy.tree.graft(app, '/')

    # Set the configuration of the web server to production mode
    cherrypy.config.update({
        'environment': 'production',
        'engine.autoreload_on': False,
        'log.screen': True,
        'server.socket_port': 5001,
        'server.socket_host': '0.0.0.0'
    })

    # Start the CherryPy WSGI web server
    cherrypy.engine.start()
    cherrypy.engine.block()
