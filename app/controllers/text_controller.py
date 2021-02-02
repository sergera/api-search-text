import json

from flask import Blueprint, request

from app.models.text_model import TextModel
from app.models.key_model import KeyModel
from app.models.query_model import QueryModel
from app.repository import repository

app_text = Blueprint('app_text', __name__)

COLLECTION_NAME = "texts"

@app_text.route('/text', methods=["POST"])
def insert():
    """
    Validates and inserts text
    """
    new_text = request.json
    text = TextModel(new_text)
    text.validate()
    unique_fields = [{"key"}]
    repository.insert_one_unique_fields(COLLECTION_NAME, text.to_dict(), unique_fields)
    return {"message": "success!"}, 201

@app_text.route('/search', methods=["GET"])
def search():
    """
    Searches for texts that match string ordered by ocurrences
    """
    args = request.args.to_dict()
    query = QueryModel(args)
    result = repository.search_text(COLLECTION_NAME, query.value)
    return {"texts": result}

@app_text.route('/text/<string:key>', methods=["GET"])
def get_by_id(key):
    """
    Gets a text by it's key
    """
    key = KeyModel(key)
    key.validate()
    return {"text": repository.get_doc(COLLECTION_NAME, key.to_dict())}
    
@app_text.route('/', methods=['GET'])
def root():
    """
    Returns a welcome message
    """
    return {"message": """Welcome to the search text API!\n
                        Use post('/text') to insert a text,\n 
                        get('/text') to get a text by key,\n 
                        and get('search') to search texts!"""}