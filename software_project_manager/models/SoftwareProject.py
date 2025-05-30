from software_project_manager import db
from datetime import datetime

class SoftwareProject(db.Model):
    __tablename__ = "software_projects"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(250), nullable=False)
    desciption = db.Column(db.String(2500), nullable=True)
    created_on = db.Column(db.DateTime, default=datetime.now())
    modified_on = db.Column(db.DateTime, default=datetime.now())
    tasks = db.relationship("Task", backref="swpr_task_id", cascade="all, delete")

    def __init__(self, name, description=None):
        self.name = name
        self.desciption = description
    
    def update(self, new_name, new_description=None):
        self.name = new_name
        self.desciption = new_description
        self.modified_on = datetime.now()
        db.session.commit()
    
    def __repr__(self):
        return f"SoftwareProject <{self.id}>"

    def to_dict(self):
        data = {
            "id": self.id,
            "name": self.name,
            "description": self.desciption,
            "created_on": self.created_on,
            "modified_on": self.modified_on
        }
        return data
