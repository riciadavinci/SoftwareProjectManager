from software_project_manager import db
from datetime import datetime

class ProjectReference(db.Model):
    __tablename__ = "project_references"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(500), nullable=False)
    url = db.Column(db.String(500), nullable=True)
    author_name = db.Column(db.String(250), nullable=False)
    created_on = db.Column(db.DateTime, default=datetime.now())
    modified_on = db.Column(db.DateTime, default=datetime.now())
    reference_type_id = db.Column(db.Integer, db.ForeignKey("project_reference_types.id"))
    software_project_id = db.Column(db.Integer, db.ForeignKey("software_projects.id"))

    def __init__(self, name, reference_type_id, software_project_id, url=None, author_name=None):
        self.name = name
        self.reference_type_id = reference_type_id
        self.software_project_id = software_project_id
        self.url = url
        self.author_name = author_name
    
    def update(self, new_name, new_reference_type_id, new_software_project_id, new_url, new_author_name):
        self.name = new_name
        self.reference_type_id = new_reference_type_id
        self.software_project_id = new_software_project_id
        self.url = new_url
        self.author_name = new_author_name
        db.session.commit()
    
    def __repr__(self):
        return f"ProjectReference <{self.id} - {self.name}> ({self.reference_type_id.name})"
    
    def to_dict(self):
        data = {
            "id": self.id,
            "name": self.name,
            "url": self.url,
            "author_name": self.author_name,
            "created_on": self.created_on,
            "modified_on": self.modified_on,
            "task_status_id": self.reference_type_id,
            "software_project_id": self.software_project_id
        }
        return data
