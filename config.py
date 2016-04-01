import os


class Config(object):
    DEBUG = os.getenv('DEBUG', True)
    AMQP_URI = os.getenv("AMQP_URI", "amqp://mquser:mqpassword@localhost:5672")
    LEGACY_ADAPTER_URI = os.getenv('LEGACY_ADAPTER_URL', 'http://localhost:5007')

