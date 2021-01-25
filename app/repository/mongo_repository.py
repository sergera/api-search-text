import pymongo
from pymongo import MongoClient

from .exceptions import (CouldNotCreateIndexException,
                         CouldNotGetDocumentException,
                         CouldNotSearchDocumentsException,
                         CouldNotInsertDocumentException,
                         ExistingDocumentException,)

INDEX_TYPES = {
    "TEXT": pymongo.TEXT,
    "HASHED": pymongo.HASHED,
}

class MongoRepository():
    """
    A class used to represent the MongoDB database
    It uses pymongo, and simplifies some of it's basic functionality

    Args:
        db_address (str):
            MongoDB's address
        db_name (str):
            The name of the database in this particular instance of MongoDB
        indexes (list[dict]):
            A list fields to be indexed in a collection with an index type
                    type:   type of index in uppercase (ex. TEXT, HASH, ...)
                    field:  field to be indexed
                    collection: collection where the field is

        Attributes:
            db_address (str):
                MongoDB's address
            db_name (str):
                the name of the database in this particular instance of MongoDB
    """
    def __init__(self, db_address, db_name, indexes=None):
        self.db_address = db_address
        self.db_name = db_name
        self._db = None
        self._client = None
        self.connect()
        if indexes:
            self.create_index(indexes)

    def connect(self):
        self._client = MongoClient(self.db_address)
        self._db = self._client[self.db_name]

    def create_index(self, indexes):
        """Creates indexes to one or more fields in one or more collections

        Args:
            indexes (list[dict]):
                A list of dictionaries with the following keys
                    type:   type of index in uppercase (ex. TEXT, HASH, ...)
                    field:  field to be indexed
                    collection: collection where the field is
                Example:
                    [{"type": "TEXT", "field": "text", "collection": "documents"}]

        Raises:
            CouldNotCreateIndexException
                If it fails to create index
        """
        for index in indexes:
            try:
                collection = index["collection"]
                field = index["field"]
                index_type = index["type"]
                self._db[collection].create_index([
                    ( field, INDEX_TYPES[index_type] )
                ])
            except:
                raise CouldNotCreateIndexException("Could not create index in collection!")

    def get_doc(self, collection_name, key):
        """Gets one document in a collection

        Args:
            collection_name (str):
                The name of the collection
            key (dict):
                one document with those keys assigned to those values will be fetched

        Returns:
            dict: Document   

        Raises:
            CouldNotGetDocumentException
                If it fails to retrieve the document
        """
        try:
            document = self._db[collection_name].find_one(key, {'_id': False})
            return document

        except:
            raise CouldNotGetDocumentException("Could not get document!")

    def search_text(self, collection_name, search_string):
        """Searchs for string in text indexed field in collection

        Args:
            collection_name (str):
                The name of the collection
            search_string (str):
                String to be matched against text indexed field

        Returns:
            list: Matched documents

        Raises:
            CouldNotSearchDocumentsException
                If it fails to search documents
        """
        try:
            cursor = self._db[collection_name].find(
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
            return list(cursor)

        except:
            raise CouldNotSearchDocumentsException("Could not searched documents!")

    def insert_one(self, collection_name, document):
        """Inserts one document in a collection

        Args:
            collection_name (str):
                Name of the collection
            document (dict):
                Document to be inserted

        Returns:
            dict: a status message

        Raises:
            CouldNotInsertDocumentException
                If it fails to insert the document
        """
        try:
            result = self._db[collection_name].insert_one(document.copy())
            return {"message": "Document Inserted!"}

        except:
            raise CouldNotInsertDocumentException("Could not insert document!")
        
    def insert_one_unique_fields(self, collection_name, document, field_sets):
        """Inserts a document with unique fields in a collection

        Args:
            collection_name (str):
                Name of the collection
            document (dict):
                Document to be inserted
            field_sets (list[set]):
                If there are no documents in the collection with any of the field_sets,
                the document will be inserted

        Raises:
            ExistingDocumentException
                In case the defined keys are not unique in the collection
        """
        for field_set in field_sets:
            unique_fields = { field: document[field] for field in field_set }
            found_document = self._db[collection_name].find_one(unique_fields, {"_id": False})
            if found_document:
                raise ExistingDocumentException("Unique fields already exists in collection!")

        message = self.insert_one(collection_name, document)
        return message