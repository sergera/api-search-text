from flask import Flask

from .controllers.text_controller import app_text
from .views.exception_handler import app_error_handler

app = Flask(__name__)
app.register_blueprint(app_text)
app.register_blueprint(app_error_handler)
