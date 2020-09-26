from flask import Flask, make_response, jsonify
from flask_restful import Resource, Api, output_json
from uuid import UUID
from . import authentication_service, user_db
# import authentication_service
# import user_db

app = Flask(__name__)
api = Api(app)

ERROR_ROLE_NOT_FOUND = "Invalid role"
ERROR_INVALID_USER_ID = "Inavlid User ID"
ERROR_INTERNAL_SERVER = "Internal Server Error"

db_config = {"user": "postgres",
             "password": "postgres",
             "host": "127.0.0.1",
             "port": "5432",
             "db_name": "user_auth"}

accepted_roles = ["admin", "user", "developer"]


def init(db_config):
    db = user_db.UserDB(db_config)
    svc = authentication_service.Authenticator(db)
    return svc


def is_valid_uuid(uuid_str):
    try:
        uuid_obj = UUID(uuid_str, version=4)
    except ValueError:
        return False

    return str(uuid_obj) == uuid_str


class Ping(Resource):
    def get(self):
        return output_json({"ping": "pong"}, 200)


class CreateUser(Resource):
    def __init__(self, svc):
        self.svc = svc

    def post(self, role):
        if role not in accepted_roles:
            return output_json({"msg": ERROR_ROLE_NOT_FOUND}, 400)

        user_details = svc.create_user(role)
        if user_details["user_created"]:
            user_details["id"] = str(user_details["id"])
            user_details["access_token"] = str(user_details["access_token"])
            return output_json(user_details, 201)
        else:
            return output_json({"msg": ERROR_INTERNAL_SERVER}, 500)


class LoginUser(Resource):
    def __init__(self, svc):
        self.svc = svc

    def put(self, user_id):
        if not is_valid_uuid(user_id):
            return output_json({"msg": ERROR_INVALID_USER_ID}, 400)

        response = svc.login(user_id)
        if response["user_logged_in"]:
            response["access_token"] = str(response["access_token"])
            return output_json(response, 201)
        elif response["error"] == user_db.ERROR_USER_NOT_FOUND:
            return output_json(response, 400)
        else:
            return output_json({"msg": ERROR_INTERNAL_SERVER}, 500)


class LogoutUser(Resource):
    def __init__(self, svc):
        self.svc = svc

    def put(self, user_id):
        if not is_valid_uuid(user_id):
            return output_json({"msg": ERROR_INVALID_USER_ID}, 400)

        response = svc.logout(user_id)
        if response["user_logged_out"]:
            return output_json(response, 200)
        elif response["error"] == user_db.ERROR_USER_NOT_FOUND:
            return output_json(response, 400)
        else:
            return output_json({"msg": ERROR_INTERNAL_SERVER}, 500)


svc = init(db_config)

api.add_resource(Ping, '/ping')
api.add_resource(CreateUser, '/auth/signup/<string:role>',
                 resource_class_kwargs={"svc": svc})
api.add_resource(LoginUser, '/auth/login/<string:user_id>',
                 resource_class_kwargs={"svc": svc})
api.add_resource(LogoutUser, '/auth/logout/<string:user_id>',
                 resource_class_kwargs={"svc": svc})

if __name__ == '__main__':
    app.run(debug=True, use_debugger=False, use_reloader=False,
            passthrough_errors=True, port=3000)
