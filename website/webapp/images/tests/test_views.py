import json
from unittest.mock import patch
import flask_testing

from webapp import app
from . import mocks
from json_api import serializers


class TestImagesEndpoints(flask_testing.TestCase):

    def create_app(self):
        return app

    def test_get_all_images(self):
        expected_response = {"data": []}
        for image in mocks.Images:
            _image = serializers.dict_serializer(
                image, fields=["id", "short_id", "tags"]
            )
            expected_response["data"].append(_image)
        mocks.DockerClient.images.list.return_value = mocks.Images
        with patch("webapp.images.views.docker.from_env", mocks.from_env):
            response = self.client.get(
                "/images", headers={"Accept": "application/json"}
            )
            self.assertEqual(response.status_code, 200)
            self.assertDictEqual(response.get_json(), expected_response)

    def test_create_new_image_with_blank_body(self):
        response = self.client.post("/images")
        self.assertEqual(
            response.headers.get("Content-Type"),
            "application/json"
        )
        self.assertEqual(response.status_code, 400)

    def test_create_new_image_without_required_param(self):
        body = {
            "attr1": "Attribute 1",
            "attr2": "Attribute 2"
        }
        response = self.client.post(
            "/images",
            data=json.dumps(body),
            headers={
                "Content-Type": "application/json",
                "Accept": "application/json"
            }
        )
        self.assertEqual(response.status_code, 400)

    def test_create_new_image(self):
        expected_response = serializers.dict_serializer(
            mocks.Images[0], fields=["id", "short_id", "tags"]
        )
        mocks.DockerClient.images.pull.return_value = mocks.Images[0]
        with patch("webapp.images.views.docker.from_env", mocks.from_env):
            response = self.client.post(
                "/images",
                data=json.dumps({"name": "test_image"}),
                headers={
                    "Content-Type": "application/json",
                    "Accept": "application/json"
                }
            )
        self.assertEqual(response.status_code, 201)
        self.assertDictEqual(response.get_json(), expected_response)

    def test_get_individual_image_not_found(self):
        mocks.DockerClient.images.get = mocks.ImageNotFound
        with patch("webapp.images.views.docker.from_env", mocks.from_env):
            response = self.client.get(
                "/images/1",
                headers={"Accept": "application/json"}
            )
            self.assertEqual(response.status_code, 404)

    def test_get_individual_image(self):
        mocks.DockerClient.images.get.return_value = mocks.Images[0]
        expected_response = serializers.dict_serializer(
            mocks.Images[0], fields=["id", "short_id", "tags"]
        )
        with patch("webapp.images.views.docker.from_env", mocks.from_env):
            response = self.client.get(
                "/images/1",
                headers={"Accept": "application/json"}
            )
            self.assertEqual(response.status_code, 200)
            self.assertDictEqual(response.get_json(), expected_response)

    def test_delete_individual_image_not_found(self):
        mocks.DockerClient.images.remove = mocks.ImageNotFound
        with patch("webapp.images.views.docker.from_env", mocks.from_env):
            response = self.client.delete(
                "/images/1",
                headers={"Accept": "application/json"}
            )
            self.assertEqual(response.status_code, 404)

    def test_delete_individual_image(self):
        mocks.DockerClient.images.delete.return_value = True
        with patch("webapp.images.views.docker.from_env", mocks.from_env):
            response = self.client.delete("/images/1")
        self.assertEqual(response.status_code, 200)
