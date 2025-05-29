from flask_restful import Resource, reqparse
from flask import jsonify, make_response, request

from software_project_manager import db
from software_project_manager import api
from software_project_manager.models import TaskStatus
from software_project_manager.models import SoftwareProject
from software_project_manager.models import Task

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

api.add_resource(TaskStatusResource, "/task-status/<string:id>")
api.add_resource(TaskStatusListResource, "/task-status/")


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
        except Exception as ex:
            return make_response(jsonify({"error_message": str(ex)}), 501)

class SoftwareProjectListResource(Resource):
    def get(self):
        data = {}
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

api.add_resource(SoftwareProjectResource, "/software-project/<int:id>")
api.add_resource(SoftwareProjectListResource, "/software-project/")
