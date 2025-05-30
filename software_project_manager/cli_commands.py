from software_project_manager import app
from software_project_manager import db
from ._app_data import DEFAULT_TASK_STATUSES, DEFAULT_REFERENCE_TYPES
from ._dummy_data import DUMMY_SOFTWARE_PROJECTS, DUMMY_TASKS
from .models import TaskStatus
from .models import SoftwareProject
from .models import Task
from .models import ProjectReferenceType


@app.cli.command("create_db")
def create_db():
    db.create_all()
    db.session.commit()

@app.cli.command("populate_db")
def pupulate_db():
    # Add default task statuses: TODO, W.I.P (Work in Progress), Done
    for id, name in DEFAULT_TASK_STATUSES.items():
        task_status = TaskStatus(id, name)
        db.session.add(task_status)
    db.session.commit()
    # ----------------------------------------
    # Add default project reference types: Youtube Video, Research Paper, Documentation, etc
    for reference_type in DEFAULT_REFERENCE_TYPES:
        project_reference_type = ProjectReferenceType(reference_type.get("name"))
        db.session.add(project_reference_type)
    db.session.commit()
    # ----------------------------------------
    # Add Dummy Software Projects:
    # Add If block to add this only during development
    for item in DUMMY_SOFTWARE_PROJECTS:
        swpr_name = item.get("name")
        swpr_description = item.get("description")
        software_project = SoftwareProject(swpr_name, swpr_description)
        db.session.add(software_project)
    db.session.commit()
    # ----------------------------------------
    # Add Dummy Tasks:
    for item in DUMMY_TASKS:
        title = item.get("title")
        description = item.get("description")
        task_status_id = item.get("task_status_id")
        software_project_id = item.get("software_project_id")
        task = Task(title, description, task_status_id, software_project_id)
        db.session.add(task)
    db.session.commit()

@app.cli.command("delete_db")
def delete_db():
    db.drop_all()
    db.session.commit()
