import datetime as dt
import time

import configargparse

from colored import fg, attr
from flask import Flask, request, jsonify, g
from flask_restful import Resource, Api, abort
from marshmallow import ValidationError
from rfc3339 import rfc3339

from user import User, UserSchema
from error import UserAlreadyExistsError, ResourceDoesNotExist, SchemaValidationError

app = Flask(__name__)
api = Api(app)

users = {}


class UserEndpoint(Resource):
    def get(self, user_id: int):
        """
        Gets a user by user id

        """
        user: User
        try:
            user = users[user_id]
        except KeyError:
            error = ResourceDoesNotExist(user_id)
            abort(error["status"], message=error["message"])

        return jsonify(user.__dict__)

    def put(self, user_id: int):
        """
        Create a user from user_id and post body
        """
        if users.get(user_id):
            error = UserAlreadyExistsError(user_id)
            abort(error["status"], message=error["message"])

        user_data = request.get_data()
        user_json = request.json

        user_json["user_id"] = user_id
        schema = UserSchema()

        try:
            result = schema.load(user_json)
        except ValidationError:
            errors = schema.validate(user_json)
            error = SchemaValidationError(user_id, errors)
            abort(
                error["status"],
                message=error["message"],
                validation_messages=error["extra"],
            )

        users[user_id] = result
        return schema.dump(result)

    def post(self, user_id: int):
        """
        Updates a user from user_id and post body
        TODO: user does not exist
        """
        user: User
        try:
            user = users[user_id]
        except KeyError:
            error = ResourceDoesNotExist(user_id)
            abort(error["status"], message=error["message"])

        user_data = request.get_data()
        user_json = request.json

        old_user_data = user.__dict__
        new_user_data = {**old_user_data, **user_json}

        schema = UserSchema()

        try:
            result = schema.load(new_user_data)
        except ValidationError:
            errors = schema.validate(user_json)
            error = SchemaValidationError(user_id, errors)
            abort(
                error["status"],
                message=error["message"],
                validation_messages=error["extra"],
            )

        users[user_id] = result
        return schema.dump(result)

    def delete(self, user_id: int):
        """
        Delete a user based on user_id
        """
        try:
            result = users.pop(user_id)
        except KeyError:
            error = ResourceDoesNotExist(user_id)
            abort(error["status"], message=error["message"])
        return schema.dump(result)


class UsersEndpoint(Resource):
    def get(self):
        """
        Gets a list of user objects from a list of user_ids

        """
        user_list = request.args.getlist("user_id")

        success = []
        errors = []
        for user_id in user_list:
            try:
                user = users[int(user_id)]
                success.append(user.__dict__)
            except KeyError:
                error = ResourceDoesNotExist(user_id)
                errors.append(error)
        result = {"successful_result": success, "errors": errors}
        return jsonify(result)

    def put(self):
        """
        Create a user from post body (expects user_id in body)
        """
        user_data = request.get_data()
        user_json = request.json

        success = []
        errors = []

        for user_object in user_json:
            user_id = user_object.get("user_id")
            if not user_id:
                message = "user_id is a required field in the post body"
                errors.append(SchemaValidationError(None, message))
                continue
            if users.get(user_id):
                errors.append(UserAlreadyExistsError(user_id))
                continue

            user_object["user_id"] = user_id
            schema = UserSchema()

            try:
                result = schema.load(user_object)
            except ValidationError:
                messages = schema.validate(user_object)
                errors.append(SchemaValidationError(user_id, messages))
                continue
            users[user_id] = result
            success.append(schema.dump(result))
        result = {"successful_result": success, "errors": errors}
        return jsonify(result)

    def post(self):
        """
        Updates a user from post body, which consists of an array of update fields
        """
        user_data = request.get_data()
        user_json = request.json

        success = []
        errors = []

        for user_object in user_json:

            user_id = user_object.get("user_id")
            if not user_id:
                message = "user_id is a required field in the post body"
                errors.append(SchemaValidationError(None, message))
                continue

            try:
                user = users[int(user_id)]
            except KeyError:
                errors.append(ResourceDoesNotExist(user_id))
                continue
            except ValueError:
                message = "user_id is must be an integer"
                errors.append(SchemaValidationError(None, message))
                continue

            old_user_data = user.__dict__
            new_user_data = {**old_user_data, **user_object}

            schema = UserSchema()

            try:
                result = schema.load(new_user_data)
            except ValidationError:
                messages = schema.validate(user_json)
                errors.append(SchemaValidationError(user_id, messages))
                continue

            users[user_id] = result
            success.append(schema.dump(result))

        result = {"successful_result": success, "errors": errors}
        return jsonify(result)

    def delete(self):
        """
        Delete a user based on list of user_ids
        """
        user_data = request.get_data()
        user_json = request.json

        success = []
        errors = []

        schema = UserSchema()

        for user_id in user_json:
            try:
                result = users.pop(int(user_id))
                success.append(schema.dump(result))
            except KeyError:
                errors.append(ResourceDoesNotExist(user_id))
                continue
            except ValueError:
                message = "user_id is must be an integer"
                errors.append(SchemaValidationError(None, message))
                continue
        result = {"successful_result": success, "errors": errors}
        return jsonify(result)


api.add_resource(UserEndpoint, "/user", "/user/<int:user_id>")
api.add_resource(UsersEndpoint, "/users")


@app.before_request
def start_timer():
    g.start = time.time()


@app.after_request
def log_request(response):
    """
    Colorful logging taken from 
    https://dev.to/rhymes/logging-flask-requests-with-colors-and-structure--7g1
    """

    now = time.time()
    duration = round(now - g.start, 2)
    now_time = dt.datetime.fromtimestamp(now)
    timestamp = rfc3339(now_time)
    ip_address = request.headers.get("X-Forwarded-For", request.remote_addr)
    host = request.host.split(":", 1)[0]
    args = dict(request.args)
    log_params = [
        ("method", request.method, "blue"),
        ("path", request.path, "blue"),
        ("status", response.status_code, "yellow"),
        ("duration", duration, "green"),
        ("time", timestamp, "magenta"),
        ("ip_address", ip_address, "red"),
        ("host", host, "red"),
        ("params", args, "blue"),
    ]

    parts = []
    for name, value, color in log_params:
        part = f"{fg(color)}{name}={value}{attr('reset')}"
        parts.append(part)
    line = " ".join(parts)

    app.logger.info(line)

    return response


if __name__ == "__main__":
    # p = configargparse.ArgParser()
    # p.add('-d', '--debug', help='Debug flag', required=False, env_var='DEBUG')  # this option can be set in a config file because it starts with '--'
    # options = p.parse_args()
    # debug = options.debug
    app.run(debug=True, port=5000)
