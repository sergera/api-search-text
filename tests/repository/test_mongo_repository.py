import unittest

import pymongo

from unittest.mock import patch
from unittest.mock import MagicMock

from app.repository.mongo_repository import MongoRepository
from app.repository.exceptions import (CouldNotCreateIndexException,
                                       CouldNotGetDocumentException,
                                       CouldNotSearchDocumentsException,
                                       CouldNotInsertDocumentException,
                                       ExistingDocumentException,)

import os
DB_NAME = os.environ.get("DB_NAME")
TEST_COLLECTION_NAME = "test"

class RepositoryTestCase(unittest.TestCase):
    """
    Tests repository interface with mocked pymongo
    """
    def setUp(self):
        #mock interface client
        self.mocked_mongo = MagicMock()
        with patch("app.repository.mongo_repository.MongoClient", self.mocked_mongo):
            self.mongo = MongoRepository("mongodb://127.0.0.1:27017", DB_NAME)
        #mock interface db
        self.mocked_db = self.mocked_mongo()[DB_NAME]
        #mock interface collection
        self.mocked_collection = MagicMock()
        self.mocked_db.__getitem__.return_value = self.mocked_collection

    def test_create_index_success(self):
        indexes = [
            {
                "type": "HASHED",
                "field": "key",
                "collection": TEST_COLLECTION_NAME
            },
            {
                "type": "TEXT",
                "field": "text",
                "collection": TEST_COLLECTION_NAME
            }
        ]
        INDEX_TYPES = {"TEXT": pymongo.TEXT, "HASHED": pymongo.HASHED}
        mocked_return_value = {"message": "success"}
        
        self.mocked_collection.create_index.return_value = mocked_return_value
        result = self.mongo.create_index(indexes)

        self.assertEqual(self.mocked_db.__getitem__.call_count, len(indexes))
        self.mocked_db.__getitem__.assert_any_call(TEST_COLLECTION_NAME)
        self.assertEqual(self.mocked_collection.create_index.call_count, len(indexes))
        self.mocked_collection.create_index.assert_any_call([
            (indexes[0]["field"], INDEX_TYPES[indexes[0]["type"]])
        ])
        self.mocked_collection.create_index.assert_any_call([
            (indexes[1]["field"], INDEX_TYPES[indexes[1]["type"]])
        ])

    def test_create_index_failure(self):
        indexes = [
            {
                "type": "HASHED",
                "field": "id",
                "collection": "documents"
            },
            {
                "type": "TEXT",
                "field": "text",
                "collection": "documents"
            }
        ]
        self.mocked_collection.create_index.side_effect = Exception("oops")

        with self.assertRaises(CouldNotCreateIndexException): 
            result = self.mongo.create_index(indexes)

    def test_get_doc_success(self):
        key = {"key": "a123", "title": "it's a title", "body": "it's a body"}
        returned_document = "i have returned"

        self.mocked_collection.find_one.return_value = returned_document

        gotten_document = self.mongo.get_doc(TEST_COLLECTION_NAME, key)

        self.mocked_db.__getitem__.assert_called_once_with(TEST_COLLECTION_NAME)
        self.mocked_collection.find_one.assert_called_once_with(key, {"_id": False})
        self.assertEqual(gotten_document, returned_document)

    def test_get_doc_failure(self):
        key = {"key": "a123", "title": "it's a title", "body": "it's a body"}

        self.mocked_collection.find_one.side_effect = Exception("oops")

        with self.assertRaises(CouldNotGetDocumentException): 
            self.mongo.get_doc(TEST_COLLECTION_NAME, key)

        self.mocked_db.__getitem__.assert_called_once_with(TEST_COLLECTION_NAME)
        self.mocked_collection.find_one.assert_called_once_with(key, {"_id": False})

    def test_search_text_success(self):
        mocked_return_value = [ 
                {"key": "a123", "title": "it's a title", "body": "it's a body"},
                {"key": "b123", "title": "it's a title", "body": "it's a body"},
                {"key": "c123", "title": "it's a title", "body": "it's a body"},
        ]
        self.mocked_collection.find.return_value = mocked_return_value

        search_string = "it's a string to be searched"
        return_value = self.mongo.search_text(TEST_COLLECTION_NAME, search_string)

        self.mocked_db.__getitem__.assert_called_once_with(TEST_COLLECTION_NAME)
        self.mocked_collection.find.assert_called_once_with(                
        {
            "$text": {
                "$search": search_string, 
                "$caseSensitive": False, 
                "$diacriticSensitive": False
                }
            }, 
            {
                '_id': False
            }
        )
        self.assertEqual(return_value, mocked_return_value)

    def test_search_text_failure(self):
        self.mocked_collection.find.side_effect = Exception("oops")

        search_string = "it's a string to be searched"
        
        with self.assertRaises(CouldNotSearchDocumentsException):
            return_value = self.mongo.search_text(TEST_COLLECTION_NAME, search_string)

    def test_insert_one_document_success(self):
        document = {"key": "a123", "title": "it's a title", "body": "it's a body"}
        returned_message = {"message": "Document Inserted!"}

        response = self.mongo.insert_one(TEST_COLLECTION_NAME, document)

        self.mocked_db.__getitem__.assert_called_once_with(TEST_COLLECTION_NAME)
        self.mocked_collection.insert_one.assert_called_once_with(document)
        self.assertEqual(returned_message, response)

    def test_insert_one_document_failure(self):
        document = {"key": "a123", "title": "it's a title", "body": "it's a body"}

        self.mocked_collection.insert_one.side_effect = Exception("oops")

        with self.assertRaises(CouldNotInsertDocumentException):
            self.mongo.insert_one(TEST_COLLECTION_NAME, document)

        self.mocked_db.__getitem__.assert_called_once_with(TEST_COLLECTION_NAME)
        self.mocked_collection.insert_one.assert_called_once_with(document)

    def test_insert_one_unique_fields(self):
        document = {"key": "a123", "title": "it's a title", "body": "it's a body"}
        unique_fields = [{"key", "title"}]
        returned_message = {"message": "Document Inserted!"}

        self.mocked_collection.find_one.return_value = None
        self.mocked_collection.insert_one.return_value = returned_message

        response = self.mongo.insert_one_unique_fields(TEST_COLLECTION_NAME, document, unique_fields)

        self.mocked_db.__getitem__.assert_called_with(TEST_COLLECTION_NAME)
        self.assertEqual(self.mocked_db.__getitem__.call_count, 2)
        self.mocked_collection.insert_one.assert_called_once_with(document)
        self.assertEqual(returned_message, response)

    def test_insert_one_unique_fields_failure(self):
        document = {"key": "a123", "title": "it's a title", "body": "it's a body"}
        unique_fields = [{"key", "title"}]

        self.mocked_collection.find_one.return_value = document
        
        with self.assertRaises(ExistingDocumentException):
            self.mongo.insert_one_unique_fields(TEST_COLLECTION_NAME, document, unique_fields)