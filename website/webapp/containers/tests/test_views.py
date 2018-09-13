import json
from unittest.mock import patch
import flask_testing

from webapp import app
from webapp.test_utils import mocks
from webapp.json_api import serializers


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

    def test_get_all_containers(self):
        expected_response = {"data": []}

        for container in mocks.Containers:
            serialized_container = serializers.dict_serializer(
                container, fields=["id", "image", "name", "short_id", "status"]
            )
            expected_response["data"].append(serialized_container)

        mocks.DockerClient.containers.list = mocks.ContainersList
        with patch("webapp.containers.views.docker.from_env", mocks.from_env):
            response = self.client.get(
                "/containers",
                headers={"Accept": "application/json"}
            )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.headers.get("Content-Type"), "application/json"
        )
        self.assertDictEqual(response.get_json(), expected_response)

    def test_get_all_containers_with_filters(self):
        expected_response = {"data": []}

        for container in mocks.Containers[:3]:
            serialized_container = serializers.dict_serializer(
                container, fields=["id", "image", "name", "short_id", "status"]
            )
            expected_response["data"].append(serialized_container)

        mocks.DockerClient.containers.list = mocks.ContainersList
        with patch("webapp.containers.views.docker.from_env", mocks.from_env):
            response = self.client.get(
                "/containers",
                query_string={"active": "true"},
                headers={"Accept": "application/json"}
            )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.headers.get("Content-Type"), "application/json"
        )
        self.assertDictEqual(response.get_json(), expected_response)

    def test_delete_container_without_id(self):
        mocks.DockerClient.containers.get = mocks.NotFound
        with patch("webapp.containers.views.docker.from_env", mocks.from_env):
            response = self.client.delete(
                "/containers/1",
                headers={"Accept": "application/json"}
            )
        self.assertEqual(response.status_code, 404)
        self.assertEqual(
            response.headers.get("Content-Type"), "application/json"
        )

    def test_delete_container_with_id(self):
        mocks.DockerClient.containers.get = mocks.SingleContainer
        with patch("webapp.containers.views.docker.from_env", mocks.from_env):
            response = self.client.delete(
                "/containers/1",
                headers={"Accept": "application/json"}
            )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.headers.get("Content-Type"), "application/json"
        )

    def test_update_container_patch_without_id(self):
        mocks.DockerClient.containers.get = mocks.NotFound
        with patch("webapp.containers.views.docker.from_env", mocks.from_env):
            response = self.client.patch(
                "/containers/1",
                headers={
                    "Accept": "application/json",
                    "Content-Type": "application/json"
                },
                data=json.dumps({"state": "start"})
            )
            self.assertEqual(response.status_code, 404)

    def test_update_container_patch_request_with_id(self):
        mocks.DockerClient.containers.get = mocks.SingleContainer
        with patch("webapp.containers.views.docker.from_env", mocks.from_env):
            response = self.client.patch(
                "/containers/1",
                headers={
                    "Accept": "application/json",
                    "Content-Type": "application/json"
                },
                data=json.dumps({"state": "start"})
            )
            self.assertEqual(response.status_code, 200)
            self.assertEqual(
                response.headers.get("Content-Type"),
                "application/json"
            )

    def test_container_create_without_valid_api_params(self):
        requests = (
            {},
            {"image": 23},
            {"image": "alpine", "command": 323},
            {"image": "alpine", "command": "echo hello world", "ports": 234},
            {"image": "alpine", "command": "echo hello world", "ports": "te"},
        )
        for request in requests:
            response = self.client.post(
                "/containers",
                headers={
                    "Accept": "application/json",
                    "Content-Type": "application/json"
                },
                data=json.dumps(request)
            )
            with self.subTest(request=request):
                self.assertEqual(response.status_code, 400)
                self.assertIn("error", response.get_json())
                self.assertEqual(
                    response.headers.get("Content-Type"),
                    "application/json"
                )

    def test_container_create_with_valid_api_params(self):
        request_data = {
            "image": "alpine:latest",
            "command": "echo hello world",
            "ports": {
                '8000': '8000'
            }
        }
        expected_response = serializers.dict_serializer(
            mocks.Containers[0],
            fields=["id", "image", "name", "short_id", "status"]
        )
        mocks.DockerClient.containers.run.return_value = mocks.Containers[0]
        with patch("webapp.containers.views.docker.from_env", mocks.from_env):
            response = self.client.post(
                "/containers",
                headers={
                    "Accept": "application/json",
                    "Content-Type": "application/json"
                },
                data=json.dumps(request_data)
            )
            self.assertEqual(response.status_code, 201)
            self.assertEqual(
                response.headers.get("Content-Type"),
                "application/json"
            )
            self.assertDictEqual(response.get_json(), expected_response)
