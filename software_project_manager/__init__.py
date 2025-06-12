from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_restful import Api
from flask_bootstrap import Bootstrap
from software_project_manager.config import Config

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)
migrate = Migrate(app, db)
api = Api(app)
Bootstrap(app)

# from models import SoftwareProject
from software_project_manager import models
from software_project_manager import apis
from software_project_manager import views
from software_project_manager import cli_commands
