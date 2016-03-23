import logging
import requests
import json
from application.routes import app
from jsonschema import validate, ValidationError


ERROR_SCHEMA = {
    "type": "object",
    "properties": {
        "type": {"type": "string"},
        "message": {"type": "string"},
        "stack": {"type": "string"},
        "subsystem": {"type": "string"}
    },
    "required": ["type", "message", "subsystem"]
}


def message_received(body, message):
    logging.info("Received new error: %s", str(body))

    # TODO: make sure it's right format for sending on...
    try:
        validate(body, ERROR_SCHEMA)
        error = body
        logging.info("Received error '{}' from {}".format(body['message'], body['subsystem']))
    except ValidationError:
        error = {
            "type": "E",
            "message": "Unknown error: " + json.dumps(body),
            "subsystem": "unknown",
            "stack": ""
        }
        logging.info("Received unknown error '{}'".format(json.dumps(body)))

    request_uri = app.config['LEGACY_ADAPTER_URI'] + '/errors'
    response = requests.post(request_uri, data=json.dumps(error), headers={'Content-Type': 'application/json'})
    logging.info('POST to /errors: %s %s', response.status_code, response.reason)
    message.ack()


def listen(incoming_connection, run_forever=True):  # pragma: no cover
    logging.info('Listening for errors')

    while True:
        try:
            incoming_connection.drain_events()
        except KeyboardInterrupt:
            logging.info("Interrupted")
            break
        if not run_forever:
            break
