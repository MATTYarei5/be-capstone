from flask import request, Blueprint

import controllers

players = Blueprint("players", __name__)


@players.route("/player", methods=["POST"])
def add_player():
    return controllers.add_player(request)


@players.route("/players", methods=["GET"])
def get_all_players():
    return controllers.get_all_players()


@players.route("/player/<player_id>", methods=["GET"])
def get_player_by_id(player_id):
    return controllers.get_player_by_id(player_id)


@players.route("/player/<player_id>", methods=["PUT"])
def update_player_by_id(player_id):
    return controllers.update_player_by_id(request, player_id)


@players.route("/player/delete/<player_id>", methods=["DELETE"])
def delete_player(player_id):
    return controllers.delete_player(player_id)
