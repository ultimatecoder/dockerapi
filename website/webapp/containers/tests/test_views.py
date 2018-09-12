from unittest.mock import patch
import flask_testing

from webapp import app
from webapp.test_utils import mocks


class TestContainerEndpoints(flask_testing.TestCase):

    def create_app(self):
        return app

    def test_getting_contain_without_id(self):
        mocks.DockerClient.containers.get = mocks.NotFound
        with patch("webapp.containers.views.docker.from_env", mocks.from_env):
            response = self.client.get(
                "/containers/1",
                headers={"Accept": "application/json"}
            )
        self.assertEqual(response.status_code, 404)

    def test_getting_container_with_id(self):
        mocks.DockerClient.containers.get = mocks.SingleContainer
        with patch("webapp.containers.views.docker.from_env", mocks.from_env):
            response = self.client.get(
                "/containers/1",
                headers={"Accept": "application/json"}
            )
        self.assertEqual(response.status_code, 200)

    def test_get_container_logs_with_unknown_id(self):
        mocks.DockerClient.containers.get = mocks.NotFound
        with patch("webapp.containers.views.docker.from_env", mocks.from_env):
            response = self.client.get(
                "/containers/1/logs",
                headers={"Accept": "application/json"}
            )
            self.assertEqual(response.status_code, 404)

    def test_get_container_logs_with_known_id(self):
        mocks.DockerClient.containers.get = mocks.SingleContainer
        with patch("webapp.containers.views.docker.from_env", mocks.from_env):
            response = self.client.get(
                "/containers/1/logs",
                headers={"Accept": "application/json"}
            )
            self.assertEqual(response.status_code, 200)
