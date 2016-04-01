from application.routes import app
from application.listener import message_received, listen
import kombu
from kombu.common import maybe_declare
from amqp import AccessRefused
import logging


def setup_incoming(hostname):
    connection = kombu.Connection(hostname=hostname)
    connection.connect()
    queue = kombu.Queue('errors')
    consumer = kombu.Consumer(connection.channel(), queues=queue, callbacks=[message_received], accept=['json'])
    consumer.consume()
    return connection, consumer


def run():
    logging.info('Run')
    hostname = app.config['AMQP_URI']
    incoming_connection, incoming_consumer = setup_incoming(hostname)

    listen(incoming_connection)
    incoming_consumer.close()
