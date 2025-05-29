from software_project_manager import db
from datetime import datetime

class TaskStatus(db.Model):
    __tablename__ = "task_statuses"
    id = db.Column(db.String(10), primary_key=True)
    name = db.Column(db.String(25), unique=True)
    created_on = db.Column(db.DateTime, default=datetime.now())
    modified_on = db.Column(db.DateTime, default=datetime.now())
    tasks = db.relationship("Task", backref="task_id")

    def __init__(self, id, name):
        self.id = id
        self.name = name
    
    def get_id(self):
        return self.id
    
    def __repr__(self):
        return f"TaskStatus <{self.id}>"
    
    def to_dict(self):
        data = {
            "id": self.id,
            "name": self.name,
            "created_on": self.created_on,
            "modified_on": self.modified_on
        }
        return data
