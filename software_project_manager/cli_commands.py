from software_project_manager import app
from software_project_manager import db


@app.cli.command("create_db")
def create_db():
    db.create_all()
    db.session.commit()

@app.cli.command("populate_db")
def add_project():
    from .models import TaskStatus
    task_statuses = {
        "todo": "TODO",
        "wip": "W.I.P",
        "done": "Done"
    }
    for id, name in task_statuses.items():
        task_status = TaskStatus(id, name)
        db.session.add(task_status)
    db.session.commit()

@app.cli.command("delete_db")
def delete_db():
    db.drop_all()
    db.session.commit()
