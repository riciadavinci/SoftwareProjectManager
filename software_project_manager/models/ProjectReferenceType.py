from software_project_manager import db
from datetime import datetime

class ProjectReferenceType(db.Model):
    __tablename__ = "project_reference_types"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(30), unique=True)
    created_on = db.Column(db.DateTime, default=datetime.now())
    modified_on = db.Column(db.DateTime, default=datetime.now())
    project_references = db.relationship("ProjectReference", backref="project_reference_id")

    def __init__(self, name):
        self.name = name
    
    def __repr__(self):
        return f"ProjectReferenceType <{self.id} - {self.name}>"
    
    def to_dict(self):
        data = {
            "id": self.id,
            "name": self.name,
            "created_on": self.created_on,
            "modified_on": self.modified_on
        }
        return data
