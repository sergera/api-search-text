from flask import Blueprint, request
import json
from app.models.document_model import DocumentModel
from app.repository import repository

app_document = Blueprint('app_document', __name__)

COLLECTION_NAME = "documents"

@app_document.route('/document', methods=["POST"])
def insert():
    """
    Validates and inserts document
    """
    new_document = request.json
    document = DocumentModel(new_document)
    document.validate()
    unique_fields = [{"key"}]
    repository.insert_one_unique_fields(COLLECTION_NAME, document.to_dict(), unique_fields)
    return {"message": "success!"}

@app_document.route('/documents/<string:search_string>', methods=["GET"])
def search(search_string):
    """
    Searches for documents that match string ordered by ocurrences
    """
    result = repository.search_text(COLLECTION_NAME, search_string)
    return {"documents": result}

@app_document.route('/document/<string:key>', methods=["GET"])
def get_by_id(key):
    """
    Gets a doc by it's key
    """
    return {"document": repository.get_doc(COLLECTION_NAME, {"key": key} )}
    
@app_document.route('/', methods=['GET'])
def root():
    """
    Returns a welcome message
    """
    return {"message": """Welcome to the search text API!\n
                        Use post('/document') to insert a document,\n 
                        get('/document') to get a doc by key,\n 
                        and get('documents') to search docs!"""}