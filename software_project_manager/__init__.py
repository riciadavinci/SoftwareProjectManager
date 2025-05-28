from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
# db = SQLAlchemy(app)

from software_project_manager import views
from software_project_manager import apis
