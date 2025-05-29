from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_restful import Api

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///software_project_manager.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)
api = Api(app)
# db.init_app()

# from models import SoftwareProject
from software_project_manager import models
from software_project_manager import apis
from software_project_manager import views
from software_project_manager import cli_commands
