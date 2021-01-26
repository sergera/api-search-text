from flask import Blueprint, request
import json
from app.models.text_model import TextModel
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
    return {"message": "success!"}

@app_text.route('/search', methods=["GET"])
def search():
    """
    Searches for texts that match string ordered by ocurrences
    """
    search_string = request.args.get("q")
    result = repository.search_text(COLLECTION_NAME, search_string)
    return {"texts": result}

@app_text.route('/text/<string:key>', methods=["GET"])
def get_by_id(key):
    """
    Gets a text by it's key
    """
    return {"text": repository.get_doc(COLLECTION_NAME, {"key": key} )}
    
@app_text.route('/', methods=['GET'])
def root():
    """
    Returns a welcome message
    """
    return {"message": """Welcome to the search text API!\n
                        Use post('/text') to insert a text,\n 
                        get('/text') to get a text by key,\n 
                        and get('search') to search texts!"""}