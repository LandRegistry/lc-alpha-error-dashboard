import logging
import requests
import json
from application.routes import app


def message_received(body, message):
    logging.info("Received new error: %s", str(body))

    # TODO: make sure it's right format for sending on...
    request_uri = app.config['LEGACY_DB_URI'] + '/errors'
    logging.info('Blah')
    response = requests.post(request_uri, data=json.dumps(body), headers={'Content-Type': 'application/json'})
    logging.info('POST to /errors: %s %s', response.status_code, response.reason)
    message.ack()


def listen(incoming_connection, run_forever=True):  # pragma: no cover
    logging.info('Listening for new registrations')

    while True:
        try:
            incoming_connection.drain_events()
        except KeyboardInterrupt:
            logging.info("Interrupted")
            break
        if not run_forever:
            break
