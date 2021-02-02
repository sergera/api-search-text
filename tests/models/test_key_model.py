import unittest

from app.models.exceptions import ValidationException
from app.models.key_model import KeyModel

class KeyModelTestCase(unittest.TestCase):
    def test_to_dict(self):
        key = "234"
        new_key = KeyModel(key)
        dict_key = new_key.to_dict()
        self.assertTrue(
            dict_key["key"] == new_key.value
        )

    def test_correct(self):
        key = "241rwfs"
        new_key = KeyModel(key)
        new_key.validate()

    def test_text_space_before(self):
        space_before_key = " a123"
        new_key = KeyModel(space_before_key)
        with self.assertRaises(ValidationException):
            new_key.validate()

    def test_text_space_after(self):
        space_after_key = "a123 "
        new_key = KeyModel(space_after_key)
        with self.assertRaises(ValidationException):
            new_key.validate()

    def test_text_space_middle(self):
        space_after_key = "a1 23 "
        new_key = KeyModel(space_after_key)
        with self.assertRaises(ValidationException):
            new_key.validate()

    def test_text_double_space(self):
        double_space = "a1  23"
        new_key = KeyModel(double_space)
        with self.assertRaises(ValidationException):
            new_key.validate()

    def test_text_dot(self):
        dot = "a1.23"
        new_key = KeyModel(dot)
        with self.assertRaises(ValidationException):
            new_key.validate()
