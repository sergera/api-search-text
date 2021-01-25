from flask import Flask

from .controllers.document_controller import app_document
from .views.exception_handler import app_error_handler

app = Flask(__name__)
app.register_blueprint(app_document)
app.register_blueprint(app_error_handler)
