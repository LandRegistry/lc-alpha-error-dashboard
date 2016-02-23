from flask import Flask, Response
import os
from log.logger import setup_logging
import logging
import json
import requests


app = Flask(__name__)
app.config.from_object('config.Config')

setup_logging(app.config['DEBUG'])


def check_legacy_health():
    return requests.get(app.config['LEGACY_DB_URI'] + '/health')


application_dependencies = [
    {
        "name": "legacy-adapter",
        "check": check_legacy_health
    }
]


@app.route('/', methods=["GET"])
def root():
    logging.info("GET /")
    return Response(status=200)


@app.route('/health', methods=['GET'])
def health():
    result = {
        'status': 'OK',
        'dependencies': {}
    }

    status = 200
    for dependency in application_dependencies:
        response = dependency["check"]()
        result['dependencies'][dependency['name']] = str(response.status_code) + ' ' + response.reason
        data = json.loads(response.content.decode('utf-8'))
        for key in data['dependencies']:
            result['dependencies'][key] = data['dependencies'][key]

    return Response(json.dumps(result), status=status, mimetype='application/json')
