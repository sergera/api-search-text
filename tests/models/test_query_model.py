import unittest

from app.models.exceptions import MissingParameterException
from app.models.query_model import QueryModel

class QueryModelTestCase(unittest.TestCase):
    def test_correct(self):
        query = {"q": "this is a query"}
        new_query = QueryModel(query)
        self.assertTrue(
            new_query.value == query["q"]
        )

    def test_missing_query(self):
        missing_query = {"v": "it's not a query", "z": "it's not a query"}
        with self.assertRaises(MissingParameterException):
            new_query = QueryModel(missing_query)
