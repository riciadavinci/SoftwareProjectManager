from software_project_manager import db
from .DbCommons import user_projects
from .DbUtils import DbUtils
from datetime import datetime
from uuid import uuid4

class UniqueUserIdGenerationError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

class UserUtils:
    @staticmethod
    def generate_unique_id():
        PREFIX = "UID"
        POSTFIX_LENGTH = 3
        uid = DbUtils.create_unique_id(PREFIX, POSTFIX_LENGTH)
        uid = str(uuid4())
        return uid


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.String(), primary_key=True, default=lambda: str(uuid4()))
    email_id = db.Column(db.String(250), unique=True, nullable=False)
    name = db.Column(db.String(250), nullable=False)
    password = db.Column(db.Text(), nullable=False)
    date_of_birth = db.Column(db.DateTime, nullable=True)
    created_on = db.Column(db.DateTime, default=lambda: datetime.now())
    modified_on = db.Column(db.DateTime, default=lambda: datetime.now())
    is_admin = db.Column(db.Boolean, default=False)
    is_developer = db.Column(db.Boolean, default=True)
    is_product_manager = db.Column(db.Boolean, default=False)
    software_projects = db.relationship("SoftwareProject", secondary=user_projects, back_populates="members")

    def __init__(self, email_id, name, password, is_developer=True, is_product_manager=False, is_admin=False, date_of_birth=None):
        self.email_id = email_id
        self.name = name
        self.password = password
        self.is_developer= is_developer
        self.is_product_manager= is_product_manager
        self.is_admin= is_admin
        self.date_of_birth = date_of_birth
    
    def update_Data(self, name, date_of_birth):
        self.name = name
        self.date_of_birth = date_of_birth
        self.modified_on = datetime.now()
        db.session.commit()
    
    def update_roles(self, is_developer, is_product_manager):
        self.is_developer= is_developer
        self.is_product_manager= is_product_manager
        self.modified_on = datetime.now()
        db.session.commit()
    
    def update_password(self, new_password):
        self.password = new_password
        self.modified_on = datetime.now()
        db.session.commit()
    
    def get_id(self):
        return self.id
    
    def __repr__(self):
        return f"User <{self.id} : {self.email_id}>"
    
    def to_dict(self):
        data = {
            "id": self.id,
            "email_id": self.email_id,
            "name": self.name,
            "created_on": self.created_on,
            "modified_on": self.modified_on,
            "date_of_birth": self.date_of_birth,
            "is_developer": self.is_developer,
            "is_product_manager": self.is_product_manager,
            "is_admin": self.is_admin
        }
        return data

