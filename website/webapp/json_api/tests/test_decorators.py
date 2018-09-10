import unittest
from unittest.mock import patch

from webapp import app
from webapp.json_api import decorators


class TestJsonAPIDecotrator(unittest.TestCase):

    def setUp(self):
        self.client = app.test_client()

    @patch("webapp.json_api.decorators.request")
    @patch("webapp.json_api.decorators.jsonify")
    def test_without_json_content(self, mocked_jsonify, mocked_request):
        mocked_request.accept_mimetypes.find.return_value = -1

        def f():
            return "Test Response"
        wrapped_function = decorators.json_api(f)
        response, status_code = wrapped_function()
        self.assertTrue(mocked_jsonify.called)
        self.assertEqual(415, status_code)

    @patch("webapp.json_api.decorators.request")
    def test_with_json_content(self, mocked_request):
        mocked_request.accept_mimetypes.find.return_value = 1
        expected_response = "Test Response"

        def f():
            return expected_response
        wrapper_function = decorators.json_api(f)
        response = wrapper_function()
        self.assertEqual(response, expected_response)

    @patch("webapp.json_api.decorators.request")
    @patch("webapp.json_api.decorators.jsonify")
    def test_it_checks_post_requests(self, mocked_jsonify, mocked_request):
        mocked_request.method = "POST"
        expected_response = "Test Response"

        def f():
            return expected_response
        wrapped_function = decorators.json_api(f)
        response, status_code = wrapped_function()
        self.assertTrue(mocked_jsonify.called)
        self.assertEqual(400, status_code)

    @patch("webapp.json_api.decorators.request")
    @patch("webapp.json_api.decorators.jsonify")
    def test_it_checks_put_requests(self, mocked_jsonify, mocked_request):
        mocked_request.method = "PUT"
        expected_response = "Test Response"

        def f():
            return expected_response
        wrapped_function = decorators.json_api(f)
        response, status_code = wrapped_function()
        self.assertTrue(mocked_jsonify.called)
        self.assertEqual(400, status_code)
