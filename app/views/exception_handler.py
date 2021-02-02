from flask import Blueprint, jsonify

from app.models.exceptions import (ValidationException,
								   MissingParameterException,)

from app.repository.exceptions import (CouldNotCreateIndexException,
									   CouldNotGetDocumentException,
									   CouldNotSearchDocumentsException,
									   CouldNotInsertDocumentException,
									   ExistingDocumentException,
									   DocumentNotFoundException,)

app_error_handler = Blueprint("app_error_handler", __name__)

@app_error_handler.app_errorhandler(MissingParameterException)
def handle_error_request_parameter(ex):
	return jsonify({"message": str(ex)}), 400

@app_error_handler.app_errorhandler(ValidationException)
def handle_error_validation(ex):
	return jsonify({"message": str(ex)}), 400

@app_error_handler.app_errorhandler(CouldNotCreateIndexException)
def handle_error_create_index(ex):
	return jsonify({"message": str(ex)}), 500

@app_error_handler.app_errorhandler(CouldNotGetDocumentException)
def handle_error_get_document(ex):
	return jsonify({"message": str(ex)}), 500

@app_error_handler.app_errorhandler(CouldNotSearchDocumentsException)
def handle_error_search_documents(ex):
	return jsonify({"message": str(ex)}), 500

@app_error_handler.app_errorhandler(CouldNotInsertDocumentException)
def handle_error_insert_document(ex):
	return jsonify({"message": str(ex)}), 500

@app_error_handler.app_errorhandler(ExistingDocumentException)
def handle_error_existing_document(ex):
	return jsonify({"message": str(ex)}), 409

@app_error_handler.app_errorhandler(DocumentNotFoundException)
def handle_error_document_not_found(ex):
	return jsonify({"message": str(ex)}), 404