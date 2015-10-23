import requests
from application.routes import app
from unittest import mock
from application.listener import message_received


class FakePublisher(object):
    def __init__(self):
        self.data = {}

    def put(self, data):
        self.data = data


class FakeResponse(requests.Response):
    def __init__(self, content='', status_code=200):
        super(FakeResponse, self).__init__()
        self._content = content
        self._content_consumed = True
        self.status_code = status_code
        self.reason = 'TEST'


class FakeMessage(object):
    def ack(self):
        pass

fake_healthcheck = FakeResponse('{"dependencies": {"an-app": "200 OK"} }'.encode(), 200)

class TestErrorReporting:
    def setup_method(self, method):
        self.app = app.test_client()

    def test_root(self):
        response = self.app.get("/")
        assert response.status_code == 200

    @mock.patch('requests.get', return_value=fake_healthcheck)
    def test_healthcheck(self, mg):
        response = self.app.get("/health")
        assert response.status_code == 200

    @mock.patch('requests.post')
    def test_message_received(self, post):
        message_received({"data": "is here"}, FakeMessage())
        assert post.call_count == 1
