import re

from .exceptions import ValidationException

ID_REGEX = re.compile("^[a-zA-Z0-9]+$")

class KeyModel():
    """
    A class used to represent a query string model
    """
    def __init__(self, key):
        """
        Args:
            key (str):
                A text key value

        Attributes:
            value (str):
                A text key value
        """
        self.value = key

    def validate(self):
        """Validates key

        Returns:
            bool: True if it is valid

        Raises:
            ValidationException
                If key is not alphanumeric
        """
        if not ID_REGEX.match(self.value):
            raise ValidationException("Key must be alphanumeric!")

    def to_dict(self):
        return {"key": self.value}