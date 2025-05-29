from software_project_manager import db
from datetime import datetime

class Task(db.Model):
    __tablename__ = "tasks"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(150), nullable=False)
    description = db.Column(db.String(300), nullable=False)
    created_on = db.Column(db.DateTime, default=datetime.now())
    modified_on = db.Column(db.DateTime, default=datetime.now())
    task_status_id = db.Column(db.String(10), db.ForeignKey("task_statuses.id"))
    software_project_id = db.Column(db.String(10), db.ForeignKey("software_projects.id"))

    def __init__(self, title, description, task_status_id, software_project_id):
        self.title = title
        self.description = description
        self.task_status_id = task_status_id
        self.software_project_id = software_project_id
    
    def update(self, new_title, new_description, new_task_status_id, software_project_id):
        self.title = new_title
        self.description = new_description
        self.task_status_id = new_task_status_id
        self.software_project_id = software_project_id
        self.modified_on = datetime.now()
        db.session.commit()
    
    def update_task_status(self, new_task_status_id):
        self.task_status_id = new_task_status_id
        self.modified_on = datetime.now()
        db.session.commit()
    
    def __repr__(self):
        return f"Task <{self.id}>"
