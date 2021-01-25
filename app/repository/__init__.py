from .mongo_repository import MongoRepository

import os
DB_ADDRESS = os.environ.get("DB_ADDRESS", "mongodb://127.0.0.1:27017")
DB_NAME = os.environ.get("DB_NAME", "api-search-text")

indexes = [
    {
        "type": "HASHED",
        "field": "key",
        "collection": "documents"
    },
    {
        "type": "TEXT",
        "field": "text",
        "collection": "documents"
    }
]


repository = MongoRepository(DB_ADDRESS, DB_NAME, indexes)