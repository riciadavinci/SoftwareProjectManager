from flask_restful import Resource, reqparse
from flask import jsonify, make_response, request
from sqlalchemy.orm.exc import UnmappedInstanceError

from software_project_manager import db
from software_project_manager import api
from software_project_manager.models import TaskStatus
from software_project_manager.models import SoftwareProject
from software_project_manager.models import Task


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
            print(type(ex))
            return make_response(jsonify({"error_message": str(ex)}), 501)
    
    def delete(self, id):
        try:
            software_project = SoftwareProject.query.get(id)
            db.session.delete(software_project)
            db.session.commit()            
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
            parser.add_argument("name")
            parser.add_argument("description")
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
        pass

    def delete(self, id):
        pass

class TaskListResource(Resource):
    def get(self):
        data = []
        try:
            parser = reqparse.RequestParser()
            parser.add_argument("swpr_id", required=False, type=int)
            parser.add_argument("user_id", required=False, type=int)
            args = parser.parse_args()
            if (args["swpr_id"]):
                data = [task_item.to_dict() for task_item in Task.query.filter_by(software_project_id=args.swpr_id)]
            else:
                data = [task_item.to_dict() for task_item in Task.query.all()]
            return make_response(jsonify({"data": data}), 200)
        except Exception as ex:
            return make_response(jsonify({"error_message": str(ex)}), 501)
    
    def post(self):
        data = []
        try:
            parser = reqparse.RequestParser()
            parser.add_argument("title", type=str)
            parser.add_argument("description", type=str)
            parser.add_argument("task_status_id", type=str)
            parser.add_argument("software_project_id", type=int)
            args = parser.parse_args()
            task = Task(args.title, args.description, args.task_status_id, args.software_project_id)
            db.session.add(task)
            db.session.commit()
            return make_response(jsonify({"data": task.to_dict()}), 200)
        except Exception as ex:
            return make_response(jsonify({"error_message": str(ex)}), 501)


api.add_resource(TaskResource, "/api/task/<int:id>")
api.add_resource(TaskListResource, "/api/task/")
