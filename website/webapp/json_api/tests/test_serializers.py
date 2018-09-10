import unittest
from unittest.mock import Mock

from .. import serializers


class TestDictSerializer(unittest.TestCase):

    def setUp(self):
        self.obj = Mock(
            attr_1="Attribute 1",
            attr_2="Attribute 2",
            attr_3="Attribute 3"
        )

    def test_object_serialize_appropriately(self):
        expected_response = {
            "attr_1": "Attribute 1",
            "attr_2": "Attribute 2"
        }
        response = serializers.dict_serializer(
            self.obj, fields=["attr_1", "attr_2"]
        )
        self.assertDictEqual(response, expected_response)
