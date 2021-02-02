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

class TextControllerTestCase(unittest.TestCase):
    """
    Tests text controller with mocked repository
    """
    def setUp(self):
        #create test client
        self.db_fd, app.app.config['DATABASE'] = tempfile.mkstemp()
        app.app.config['TESTING'] = True
        self.test_app = app.app.test_client()
        #mock repository
        self.mocked_repository = MagicMock()

    def test_post_text(self):
        mocked_response = {"message": "success!"}
        text_to_insert = {"key": "a123", "title": "it's a title", "body": "it's a body"}
        with patch("app.controllers.text_controller.repository", self.mocked_repository):
            self.mocked_repository.insert_one.return_value = mocked_response
            response = self.test_app.post(
                "/text",
                data=json.dumps(text_to_insert, indent=4),
                content_type="application/json"
            )

            statuscode = response.status_code
            self.assertEqual(response.content_type, "application/json")
            self.assertEqual(statuscode, 201)
            self.assertTrue(b"message" in response.data)
            translated_json = json.loads(response.data)
            self.assertEqual(translated_json, mocked_response)     

    def test_search_text(self):
        mocked_response = [{"key": "a123", "title": "it's a title", "body": "it's a body"}]
        text_to_insert = {"key": "a123", "title": "it's a title", "body": "it's a body"}
        with patch("app.controllers.text_controller.repository", self.mocked_repository):
            self.mocked_repository.search_text.return_value = mocked_response
            response = self.test_app.get(
                f"/search?q={text_to_insert['title']}",
                content_type="application/json"
            )

            statuscode = response.status_code
            self.assertEqual(response.content_type, "application/json")
            self.assertEqual(statuscode, 200)
            self.assertTrue(b"texts" in response.data)
            translated_json = json.loads(response.data)
            self.assertEqual(translated_json, {"texts": mocked_response})            

    def test_search_text_missing_query_string(self):
        text_to_insert = {"key": "a123", "title": "it's a title", "body": "it's a body"}
        response = self.test_app.get(
            f"/search?v={text_to_insert['title']}",
            content_type="application/json"
        )

        statuscode = response.status_code
        self.assertEqual(statuscode, 400)

    def test_get_by_id(self):
        mocked_response = {"key": "a123", "title": "it's a title", "body": "it's a body"}
        text_key = "a123"
        with patch("app.controllers.text_controller.repository", self.mocked_repository):
            self.mocked_repository.get_doc.return_value = mocked_response
            response = self.test_app.get(
                f"/text/{text_key}",
                content_type="application/json"
            )

            statuscode = response.status_code
            self.assertEqual(response.content_type, "application/json")
            self.assertEqual(statuscode, 200)
            self.assertTrue(b"text" in response.data)
            translated_json = json.loads(response.data)
            self.assertEqual(translated_json, {"text": mocked_response})            
            