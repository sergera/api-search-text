import unittest

from app.models.exceptions import ValidationException
from app.models.document_model import DocumentModel


class DocumentModelTestCase(unittest.TestCase):
    """A Test of the Validation Regex
    
    Testing if the key regex pattern is responding as intended
    """
    def test_correct(self):
        correct = {"key": "a123", "title": "it's a title", "body": "it's a body"}
        new_document =  DocumentModel(correct)
        self.assertTrue(new_document.validate())

    def test_to_dict(self):
        correct = {"key": "a123", "title": "it's a title", "body": "it's a body"}
        new_document =  DocumentModel(correct)
        document_dict = new_document.to_dict()
        self.assertTrue(
            document_dict["key"] == correct["key"] and 
            document_dict["title"] == correct["title"] and
            document_dict["body"] == correct["body"])

    def test_document_space_before(self):
        space_before_key = {"key": " a123", "title": "it's a title", "body": "it's a body"}
        new_document =  DocumentModel(space_before_key)
        with self.assertRaises(ValidationException):
            new_document.validate()

    def test_document_space_after(self):
        space_after_key = {"key": "a123 ", "title": "it's a title", "body": "it's a body"}
        new_document =  DocumentModel(space_after_key)
        with self.assertRaises(ValidationException):
            new_document.validate()

    def test_document_space_middle(self):
        space_after_key = {"key": "a1 23 ", "title": "it's a title", "body": "it's a body"}
        new_document =  DocumentModel(space_after_key)
        with self.assertRaises(ValidationException):
            new_document.validate()

    def test_document_double_space(self):
        double_space = {"key": "a1  23", "title": "it's a title", "body": "it's a body"}
        new_document =  DocumentModel(double_space)
        with self.assertRaises(ValidationException):
            new_document.validate()

    def test_document_dot(self):
        dot = {"key": "a1.23", "title": "it's a title", "body": "it's a body"}
        new_document =  DocumentModel(dot)
        with self.assertRaises(ValidationException):
            new_document.validate()