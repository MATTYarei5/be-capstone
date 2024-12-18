from flask import request, Blueprint

import controllers

games = Blueprint("games", __name__)


@games.route("/game", methods=["POST"])
def add_game():
    return controllers.add_game(request)


@games.route("/games", methods=["GET"])
def get_all_games():
    return controllers.get_all_games()


@games.route("/game/<game_id>", methods=["GET"])
def get_game_by_id(game_id):
    return controllers.get_game_by_id(game_id)


@games.route("/game/<game_id>", methods=["PUT"])
def update_game_by_id(game_id):
    return controllers.update_game_by_id(request, game_id)


@games.route("/game/delete/<game_id>", methods=["DELETE"])
def delete_game(game_id):
    return controllers.delete_game(game_id)
