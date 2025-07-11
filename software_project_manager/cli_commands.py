import click
from software_project_manager import app
from software_project_manager import db
from werkzeug.security import generate_password_hash
from ._app_data import DEFAULT_TASK_STATUSES, DEFAULT_REFERENCE_TYPES, DEFAULT_SOFTWARE_PROJECTS, DEFAULT_PROJECT_REFERENCES
from ._dummy_data import DUMMY_SOFTWARE_PROJECTS, DUMMY_TASKS, DUMMY_USERS
from .models import User
from .models import TaskStatus
from .models import SoftwareProject
from .models import Task
from .models import ProjectReferenceType
from .models import ProjectReference


@app.cli.command("create_db")
def create_db():
    db.create_all()
    db.session.commit()

@app.cli.command("populate_db")
def pupulate_db():
    # ----------------------------------------
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
    # Add default projects: just the project itself atm ("Software Project Manager"):
    for project_item in DEFAULT_SOFTWARE_PROJECTS:
        name = project_item.get("name")
        description = project_item.get("description")
        sw_project = SoftwareProject(name, description)
        db.session.add(sw_project)
    db.session.commit()
    # ----------------------------------------
    # Add default project references (for "Software Project Manager"):
    for project_ref_item in DEFAULT_PROJECT_REFERENCES:
        name = project_ref_item.get("name")
        reference_type_id = project_ref_item.get("reference_type_id")
        software_project_id = project_ref_item.get("software_project_id")
        url = project_ref_item.get("url")
        author = project_ref_item.get("author")
        project_reference = ProjectReference(name, reference_type_id, software_project_id, url, author)
        db.session.add(project_reference)
    db.session.commit()

@app.cli.command("insert_dummy_data")
def insert_dummy_data():
    # ----------------------------------------
    # Adding dummy users:
    for item in DUMMY_USERS:
        name = item.get("name")
        email_id = item.get("email_id")
        password = item.get("password")
        is_developer = item.get("is_developer")
        is_product_manager = item.get("is_product_manager")
        password_hash = generate_password_hash(password, method="scrypt")
        user = User(email_id, name, password_hash, is_developer, is_product_manager)
        db.session.add(user)
        print(user)
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

@app.cli.command("add_admin")
@click.argument("email")
@click.argument("name")
@click.argument("password")
def add_admin(email, name, password):
    # ----------------------------------------
    # Add Admin User:
    password_hash = generate_password_hash(password, method="scrypt")
    admin_user = User(email, name, password_hash, True, True, True)
    db.session.add(admin_user)
    db.session.commit()
    print(admin_user)

@app.cli.command("delete_db")
def delete_db():
    db.drop_all()
    db.session.commit()
