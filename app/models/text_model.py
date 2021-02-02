from .exceptions import (ValidationException,
                        MissingParameterException,)

from .key_model import KeyModel

class TextModel():
    """
    A class used to represent a text document model
    """
    def __init__(self, text):
        """
        Args:
            text (dict):
                A dict containing the "key", "title" and "body" keys

        Attributes:
            key (str):
                Text's id (must be alphanumeric)
            title (str):
                Text title
            body (str):
                Text body

        Raises:
            MissingParameterException
                If text doesn't have the "key", "title", or "body" keys
        """
        try:
            self.key = KeyModel(text["key"])
            self.title = text["title"]
            self.body = text["body"]
        except:
            raise MissingParameterException("Text must have 'key','title', and 'body'!")

        self.text = f"{self.title} {self.body}"

    def validate(self):
        """
        Validates key
        """
        self.key.validate()

    def to_dict(self):
        """Makes a dict out of this object

        Returns:
            dict: with each key as a property from this object
        """
        return {"key": self.key.value, "title": self.title, "body": self.body, "text": self.text}