import re

from .exceptions import ValidationException

ID_REGEX = re.compile("^[a-zA-Z0-9]+$")

class DocumentModel():
    """
    A class used to represent a document model

    Args:
        document (dict):
            A dict containing the "key", "title" and "body" keys

    Attributes:
        key (str):
            Document's id (must be alphanumeric)
        title (str):
            Document title
        body (str):
            Document body
    """
    def __init__(self, document):
        try:
            self.key = document["key"]
            self.title = document["title"]
            self.body = document["body"]
        except:
            raise ValidationException("Missing Parameters!")

        self.text = f"{self.title} {self.body}"

    def validate(self):
        """Validates document properties

        Returns:
            bool: True if it is valid

        Raises:
            ValidationException
                If any of the properties are not valid
        """
        if not ID_REGEX.match(self.key):
            raise ValidationException("Key not valid!")

        return True

    def to_dict(self):
        """Makes a dict out of this object

        Returns:
            dict: with each key as a property from this object
        """
        return {"key": self.key, "title": self.title, "body": self.body, "text": self.text}