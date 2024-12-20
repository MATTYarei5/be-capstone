from flask import request, Blueprint

import controllers


user = Blueprint('user', __name__)


@user.route("/user", methods=['POST'])
def add_user():
    return controllers.add_user(request)


@user.route("/users", methods=['GET'])
def get_all_users():
    return controllers.get_all_users(request)


@user.route("/user/<user_id>", methods=['GET'])
def get_user_by_id(user_id):
    return controllers.get_user_by_id(user_id)


@user.route("/user/<user_id>", methods=['PUT'])
def update_user_by_id(user_id):
    return controllers.update_user_by_id(request, user_id)


@user.route("/user/delete/<user_id>", methods=['DELETE'])
def delete_user(user_id):
    return controllers.delete_user(user_id)
