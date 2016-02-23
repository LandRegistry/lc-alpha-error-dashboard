import os


class Config(object):
    DEBUG = os.getenv('DEBUG', True)
    MQ_USERNAME = os.getenv("MQ_USERNAME", "mquser")
    MQ_PASSWORD = os.getenv("MQ_PASSWORD", "mqpassword")
    MQ_HOSTNAME = os.getenv("MQ_HOST", "localhost")
    MQ_PORT = os.getenv("MQ_PORT", "5672")
    LEGACY_ADAPTER_URI = os.getenv('LEGACY_ADAPTER_URL', 'http://localhost:5007')

