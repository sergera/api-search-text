import tempfile
import unittest
from unittest.mock import patch
from unittest.mock import MagicMock
import json

import os
DB_NAME = os.environ.get("DB_NAME")

from app.repository import repository
from app.repository.mongo_repository import MongoRepository
from app import app

class DocumentControllerTestCase(unittest.TestCase):
    """
    Tests document controller with mocked repository
    """
    def setUp(self):
        #create test client
        self.db_fd, app.app.config['DATABASE'] = tempfile.mkstemp()
        app.app.config['TESTING'] = True
        self.test_app = app.app.test_client()
        #mock repository
        self.mocked_repository = MagicMock()

    def test_post_document(self):
        mocked_response = {"message": "success!"}
        document_to_insert = {"key": "a123", "title": "it's a title", "body": "it's a body"}
        with patch("app.controllers.document_controller.repository", self.mocked_repository):
            self.mocked_repository.insert_one.return_value = mocked_response
            response = self.test_app.post(
                "/document",
                data=json.dumps(document_to_insert, indent=4),
                content_type="application/json"
            )

            statuscode = response.status_code
            self.assertEqual(response.content_type, "application/json")
            self.assertEqual(statuscode, 200)
            self.assertTrue(b"message" in response.data)
            translated_json = json.loads(response.data)
            self.assertEqual(translated_json, mocked_response)     

    def test_search_document(self):
        mocked_response = [{"key": "a123", "title": "it's a title", "body": "it's a body"}]
        document_to_insert = {"key": "a123", "title": "it's a title", "body": "it's a body"}
        with patch("app.controllers.document_controller.repository", self.mocked_repository):
            self.mocked_repository.search_text.return_value = mocked_response
            response = self.test_app.get(
                f"/documents/{document_to_insert['title']}",
                data=json.dumps(document_to_insert, indent=4),
                content_type="application/json"
            )

            statuscode = response.status_code
            self.assertEqual(response.content_type, "application/json")
            self.assertEqual(statuscode, 200)
            self.assertTrue(b"documents" in response.data)
            translated_json = json.loads(response.data)
            self.assertEqual(translated_json, {"documents": mocked_response})            
            
    def test_get_by_id(self):
        mocked_response = {"key": "a123", "title": "it's a title", "body": "it's a body"}
        document_key = {"key": "a123"}
        with patch("app.controllers.document_controller.repository", self.mocked_repository):
            self.mocked_repository.get_doc.return_value = mocked_response
            response = self.test_app.get(
                f"/document/{document_key}",
                content_type="application/json"
            )

            statuscode = response.status_code
            self.assertEqual(response.content_type, "application/json")
            self.assertEqual(statuscode, 200)
            self.assertTrue(b"document" in response.data)
            translated_json = json.loads(response.data)
            self.assertEqual(translated_json, {"document": mocked_response})            
            