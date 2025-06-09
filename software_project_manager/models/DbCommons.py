from software_project_manager import db

user_projects = db.Table(
    "user_projects",
    db.Column("user_id", db.String(), db.ForeignKey("users.id"), primary_key=True),
    db.Column("sw_project_id", db.Integer, db.ForeignKey("software_projects.id"), primary_key=True)
)
