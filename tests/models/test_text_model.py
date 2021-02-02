import unittest

from app.models.exceptions import MissingParameterException
from app.models.text_model import TextModel


class TextModelTestCase(unittest.TestCase):
    """A Test of the Validation Regex
    
    Testing if the key regex pattern is responding as intended
    """
    def test_correct(self):
        correct = {"key": "a123", "title": "it's a title", "body": "it's a body"}
        new_text = TextModel(correct)
        new_text.validate()

    def test_to_dict(self):
        correct = {"key": "a123", "title": "it's a title", "body": "it's a body"}
        new_text = TextModel(correct)
        text_dict = new_text.to_dict()
        self.assertTrue(
            text_dict["key"] == correct["key"] and 
            text_dict["title"] == correct["title"] and
            text_dict["body"] == correct["body"]
        )

    def test_missing_key(self):
        missing_key = {"title": "it's a title", "body": "it's a body"}
        with self.assertRaises(MissingParameterException):
            new_text = TextModel(missing_key)

    def test_missing_title(self):
        missing_title = {"key": "a1.23", "body": "it's a body"}
        with self.assertRaises(MissingParameterException):
            new_text = TextModel(missing_title)

    def test_missing_body(self):
        missing_body = {"key": "a1.23", "title": "it's a title"}
        with self.assertRaises(MissingParameterException):
            new_text = TextModel(missing_body)