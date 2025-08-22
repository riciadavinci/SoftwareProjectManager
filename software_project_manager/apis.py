from flask_restful import Resource, reqparse
from flask import jsonify, make_response, request
from sqlalchemy.orm.exc import UnmappedInstanceError
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity, get_jwt
from datetime import timedelta

from software_project_manager import db
from software_project_manager import api
from software_project_manager.models import TaskStatus
from software_project_manager.models import SoftwareProject
from software_project_manager.models import Task
from software_project_manager.models import ProjectReference
from software_project_manager.models import User


def nullable_int(value):
    if value in (None, ""):
        return None
    return int(value)

# ----------------------------------------
# 'Login/Logout/Refresh' API
# ----------------------------------------

class LoginResource(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("email_id", type=str, required=True)
        parser.add_argument("password", type=str, required=True)
        args = parser.parse_args()
        email_id = args.get("email_id")
        password = args.get("password")
        user = User.query.filter_by(email_id=email_id).first()
        if not user:
            return make_response(jsonify({"error": "Invalid Email-id"}), 401)
        if check_password_hash(user.password, password):
            access_token = create_access_token(identity=user.id, expires_delta=timedelta(minutes=15))
            refresh_token = create_refresh_token(identity=user.id, expires_delta=timedelta(days=15))
            resp = make_response(jsonify({"access_token": access_token, "refresh_token": refresh_token}), 200)
            resp.set_cookie("access_token_cookie", access_token, httponly=True, samesite='Lax')
            resp.set_cookie("refresh_token_cookie", refresh_token, httponly=True, samesite='Lax')
            return resp

class LogoutResource(Resource):
    def post(self):
        resp = make_response(jsonify({"message": "logged out"}), 201)
        resp.delete_cookie("access_token_cookie")
        resp.delete_cookie("refresh_token_cookie")
        return resp

class RefreshTokenResource(Resource):
    @jwt_required(refresh=True)
    def post(self):
        user = get_jwt_identity()
        access_token = create_access_token(identity=user, expires_delta=timedelta(minutes=15))
        resp = make_response(jsonify({"access_token": access_token}), 201)
        resp.set_cookie("access_token_cookie", access_token, httponly=True, samesite='Lax')
        return resp

api.add_resource(LoginResource, "/api/login")
api.add_resource(LogoutResource, "/api/logout")
api.add_resource(RefreshTokenResource, "/api/refresh-token")


# ----------------------------------------
# 'TaskStatus' API:
# ----------------------------------------

class TaskStatusResource(Resource):
    def get(self, id):
        data = {}
        try:
            task_status = TaskStatus.query.get(id)
            data = task_status.to_dict()
            return make_response(jsonify({"data": data}), 200)
        except Exception as ex:
            return make_response(jsonify({"error_message": str(ex)}), 501)

class TaskStatusListResource(Resource):
    def get(self):
        data = []
        try:
            data = [task_status_item.to_dict() for task_status_item in TaskStatus.query.all()]
            return make_response(jsonify({"data": data}), 200)
        except Exception as ex:
            return make_response(jsonify({"error_message": str(ex)}), 501)

api.add_resource(TaskStatusResource, "/api/task-status/<string:id>")
api.add_resource(TaskStatusListResource, "/api/task-status/")


# ----------------------------------------
# 'SoftwareProject' API:
# ----------------------------------------

class SoftwareProjectResource(Resource):
    def get(self, id):
        data = {}
        try:
            software_project = SoftwareProject.query.get(id)
            data = software_project.to_dict()
            return make_response(jsonify({"data": data}), 200)
        except AttributeError as ex:
            return make_response(jsonify({"error_message": f"SoftwareProject <{id}> not found!"}), 404)
        except Exception as ex:
            return make_response(jsonify({"error_message": str(ex)}), 501)
    
    def put(self, id):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument("name", type=str, required=True)
            parser.add_argument("description", type=str, required=True)
            args = parser.parse_args()
            software_project = SoftwareProject.query.get(id)
            if software_project:
                software_project.update(args["name"], args["description"])
            data = software_project.to_dict()
            return make_response(jsonify({"data": data}), 200)
        except AttributeError as ex:
            return make_response(jsonify({"error_message": f"SoftwareProject <{id}> not found!"}), 404)
        except UnmappedInstanceError as ex:
            return make_response(jsonify({"error_message": f"SoftwareProject <{id}> not found! Therefore, cannot update it."}), 404)
        except Exception as ex:
            return make_response(jsonify({"error_message": str(ex)}), 501)
    
    def delete(self, id):
        try:
            software_project = SoftwareProject.query.get(id)
            if software_project:
                db.session.delete(software_project)
                db.session.commit()
                # No need to delete all Tasks, ProjectReferences, and SoftwareBugs related to this particular project, 
                # because cascade="all, delete" in the db.relationship() will take care of all these.
            return make_response(jsonify({"message": f"Deleted {software_project}"}))
        except UnmappedInstanceError as ex:
            return make_response(jsonify({"error_message": f"SoftwareProject <{id}> not found! Therefore, cannot delete it."}), 404)
        except Exception as ex:
            return make_response(jsonify({"error_message": str(ex)}), 501)

class SoftwareProjectListResource(Resource):
    def get(self):
        data = []
        try:
            data = [software_project_item.to_dict() for software_project_item in SoftwareProject.query.all()]
            return make_response(jsonify({"data": data}), 200)
        except Exception as ex:
            return make_response(jsonify({"error_message": str(ex)}), 501)
    
    def post(self):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument("name", type=str, required=True)
            parser.add_argument("description", type=str, required=True)
            args = parser.parse_args()
            software_project = SoftwareProject(args.name, args.description)
            db.session.add(software_project)
            db.session.commit()
            return make_response(jsonify({"data": software_project.to_dict()}), 200)
        except Exception as ex:
            return make_response(jsonify({"error_message": str(ex)}), 501)

api.add_resource(SoftwareProjectResource, "/api/software-project/<int:id>")
api.add_resource(SoftwareProjectListResource, "/api/software-project/")


# ----------------------------------------
# 'Task' API:
# ----------------------------------------

class TaskResource(Resource):
    def get(self, id):
        data = {}
        try:
            task = Task.query.get(id)
            data = task.to_dict()
            return make_response(jsonify({"data": data}), 200)
        except AttributeError as ex:
                return make_response(jsonify({"error_message": f"Task <{id}> not found!"}), 404)
        except Exception as ex:
            return make_response(jsonify({"error_message": str(ex)}), 501)
    
    def put(self, id):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument("title", type=str, required=True)
            parser.add_argument("description", type=str, required=True)
            parser.add_argument("task_status_id", type=str, required=True)
            parser.add_argument("software_project_id", type=int, required=True)
            args = parser.parse_args()
            task = Task.query.get(id)
            if task:
                task.update(args["title"], args["description"], args["task_status_id"], args["software_project_id"])
            data = task.to_dict()
            return make_response(jsonify({"data": data}), 200)
        except UnmappedInstanceError as ex:
            return make_response(jsonify({"error_message": f"Task <{id}> not found! Therefore, cannot update it."}), 404)
        except Exception as ex:
            return make_response(jsonify({"error_message": str(ex)}), 501)

    def delete(self, id):
        try:
            task = Task.query.get(id)
            db.session.delete(task)
            db.session.commit()            
            return make_response(jsonify({"message": f"Deleted {task}"}))
        except UnmappedInstanceError as ex:
                return make_response(jsonify({"error_message": f"Task <{id}> not found! Therefore, cannot delete it."}), 404)
        except Exception as ex:
            return make_response(jsonify({"error_message": str(ex)}), 501)

class TaskListResource(Resource):
    @jwt_required()
    def get(self):
        data = []
        try:
            parser = reqparse.RequestParser()
            parser.add_argument("swpr_id", required=False, type=nullable_int, location="args")
            parser.add_argument("user_id", required=False, type=nullable_int, location="args")
            args = parser.parse_args()
            swpr_id = args.get("swpr_id")
            user_id = args.get("user_id")
            if (swpr_id):
                swpr_id = int(swpr_id)
                data = [task_item.to_dict() for task_item in Task.query.filter_by(software_project_id=swpr_id)]
            else:
                data = [task_item.to_dict() for task_item in Task.query.all()]
            return make_response(jsonify({"data": data}), 200)
        except Exception as ex:
            return make_response(jsonify({"error_message": str(ex)}), 501)
    
    def post(self):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument("title", type=str, required=True)
            parser.add_argument("description", type=str, required=True)
            parser.add_argument("task_status_id", type=str, required=True)
            parser.add_argument("software_project_id", type=int, required=True)
            args = parser.parse_args()
            task = Task(args["title"], args["description"], args["task_status_id"], args["software_project_id"])
            db.session.add(task)
            db.session.commit()
            return make_response(jsonify({"data": task.to_dict()}), 200)
        except Exception as ex:
            return make_response(jsonify({"error_message": str(ex)}), 501)


api.add_resource(TaskResource, "/api/task/<int:id>")
api.add_resource(TaskListResource, "/api/task")


class TaskStatusUpdateResource(Resource):
    @jwt_required()
    def patch(self, id):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument("task_status_id", type=str, required=True)
            args = parser.parse_args()
            task = Task.query.get(id)
            if task:
                new_status = args.get("task_status_id")
                task.update_task_status(new_status)
            data = task.to_dict()
            return make_response(jsonify({"data": data}), 200)
        except UnmappedInstanceError as ex:
            return make_response(jsonify({"error_message": f"Task <{id}> not found! Therefore, cannot update its Status."}), 404)
        except Exception as ex:
            return make_response(jsonify({"error_message": str(ex)}), 501)

api.add_resource(TaskStatusUpdateResource, "/api/task/<int:id>/status")

# ----------------------------------------
# 'ProjectReference' API
# ----------------------------------------

class ProjectReferenceResource(Resource):
    def get(self, id):
        data = {}
        try:
            project_ref = ProjectReference.query.get(id)
            data = project_ref.to_dict()
            return make_response(jsonify({"data": data}), 200)
        except AttributeError as ex:
                return make_response(jsonify({"error_message": f"ProjectReference <{id}> not found!"}), 404)
        except Exception as ex:
            return make_response(jsonify({"error_message": str(ex)}), 501)

    def put(self, id):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument("name", type=str, required=True)
            parser.add_argument("reference_type_id", type=str, required=True)
            parser.add_argument("software_project_id", type=int, required=True)
            parser.add_argument("url", type=str, required=False)
            parser.add_argument("author_name", type=str, required=False)
            args = parser.parse_args()
            project_ref = ProjectReference.query.get(id)
            if project_ref:
                project_ref.update(args["name"], args["reference_type_id"], args["software_project_id"], args["url"], args["author_name"])
            data = project_ref.to_dict()
            return make_response(jsonify({"data": data}), 200)
        except UnmappedInstanceError as ex:
            return make_response(jsonify({"error_message": f"ProjectReference <{id}> not found! Therefore, cannot update it."}), 404)
        except Exception as ex:
            return make_response(jsonify({"error_message": str(ex)}), 501)

    def delete(self, id):
        try:
            project_ref = ProjectReference.query.get(id)
            db.session.delete(project_ref)
            db.session.commit()            
            return make_response(jsonify({"message": f"Deleted ProjectReference <{id}>!"}))
        except UnmappedInstanceError as ex:
                return make_response(jsonify({"error_message": f"ProjectReference <{id}> not found! Therefore, cannot delete it."}), 404)
        except Exception as ex:
            return make_response(jsonify({"error_message": str(ex)}), 501)

class ProjectReferenceListResource(Resource):
    def get(self):
        data = []
        try:
            parser = reqparse.RequestParser()
            parser.add_argument("swpr_id", required=False, type=int)
            args = parser.parse_args()
            if (args["swpr_id"]):
                data = [pr_ref_item.to_dict() for pr_ref_item in ProjectReference.query.filter_by(software_project_id=args.swpr_id)]
            else:
                data = [pr_ref_item.to_dict() for pr_ref_item in ProjectReference.query.all()]
            return make_response(jsonify({"data": data}), 200)
        except Exception as ex:
            return make_response(jsonify({"error_message": str(ex)}), 501)

    def post(self):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument("name", type=str, required=True)
            parser.add_argument("reference_type_id", type=str, required=True)
            parser.add_argument("software_project_id", type=int, required=True)
            parser.add_argument("url", type=str, required=False)
            parser.add_argument("author_name", type=str, required=False)
            args = parser.parse_args()
            project_reference = ProjectReference(args["name"], args["reference_type_id"], args["software_project_id"], args["url"], args["author_name"])
            db.session.add(project_reference)
            db.session.commit()
            return make_response(jsonify({"data": project_reference.to_dict()}), 200)
        except Exception as ex:
            return make_response(jsonify({"error_message": str(ex)}), 501)


api.add_resource(ProjectReferenceResource, "/api/project-reference/<int:id>")
api.add_resource(ProjectReferenceListResource, "/api/project-reference/")


# ----------------------------------------
# 'ProjectReferenceType' API
# ----------------------------------------

