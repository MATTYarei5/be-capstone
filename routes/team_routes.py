from flask import request, Blueprint

import controllers

teams = Blueprint("teams", __name__)


@teams.route("/team", methods=["POST"])
def add_team():
    return controllers.add_team(request)


@teams.route("/teams", methods=["GET"])
def get_all_teams():
    return controllers.get_all_teams()


@teams.route("/team/<team_id>", methods=["GET"])
def get_team_by_id(team_id):
    return controllers.get_team_by_id(team_id)


@teams.route("/team/<team_id>", methods=["PUT"])
def update_team_by_id(team_id):
    return controllers.update_team_by_id(request, team_id)


@teams.route("/team/delete/<team_id>", methods=["DELETE"])
def delete_team(team_id):
    return controllers.delete_team(team_id)
