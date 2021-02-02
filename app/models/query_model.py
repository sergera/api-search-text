from .exceptions import MissingParameterException

class QueryModel():
    """
    A class used to represent a query string model
    """
    def __init__(self, query):
        """
        Args:
            query (dict):
                A dict containing the "q" key

        Attributes:
            query (str):
                A query string

        Raises: 
            MissingParameterException
                If query doesn't have the "q" parameter
        """
        try:
            self.value = query["q"]
        except:
            raise MissingParameterException("Missing parameter 'q' in URL query string!")
