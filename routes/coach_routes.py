from flask import request, Blueprint

import controllers

coaches = Blueprint("coaches", __name__)


@coaches.route("/coach", methods=["POST"])
def add_coach():
    return controllers.add_coach(request)


@coaches.route("/coaches", methods=["GET"])
def get_all_coaches():
    return controllers.get_all_coaches(request)


@coaches.route("/coach/<coach_id>", methods=["GET"])
def get_coach_by_id(coach_id):
    return controllers.get_coach_by_id(coach_id)


@coaches.route("/coach/<coach_id>", methods=["PUT"])
def update_coach_by_id(coach_id):
    return controllers.update_coach_by_id(request, coach_id)


@coaches.route("/coach/delete/<coach_id>", methods=["DELETE"])
def delete_coach(coach_id):
    return controllers.delete_coach(coach_id)
