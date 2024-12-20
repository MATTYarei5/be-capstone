from flask import jsonify, request

from models.game import Game, game_schema, games_schema
from models.team import Team
from util.reflection import populate_object
from lib.authenticate import authenticate_return_auth, auth

from db import db


@authenticate_return_auth
def add_game(request, auth_info):

    if auth_info.user.role != 'super-admin':
        return jsonify({"message": "unauthorized"}), 401

    post_data = request.form if request.form else request.json
    home_team = post_data.get('home_team_id')
    away_team = post_data.get('away_team_id')

    if home_team == away_team:
        return jsonify({"message": "home team and away team cannot be the same"}), 400

    if home_team == None or away_team == None:
        return jsonify({"message": "home team and away team must be provided"}), 400

    home_team_query = db.session.query(Team).filter(Team.team_id == home_team).first()
    away_team_query = db.session.query(Team).filter(Team.team_id == away_team).first()

    new_game = Game.new_game_obj()

    populate_object(new_game, post_data)

    new_game.teams.append(home_team_query)
    new_game.teams.append(away_team_query)

    db.session.add(new_game)
    db.session.commit()

    return jsonify({"message": "game created", "result": game_schema.dump(new_game)}), 201


@auth
def get_all_games():
    games_query = db.session.query(Game).all()

    return jsonify({"message": "games retrieved", "result": games_schema.dump(games_query)}), 200


@auth
def get_game_by_id(game_id):
    game_query = db.session.query(Game).filter(Game.game_id == game_id).first()

    if not game_query:
        return jsonify({"message": "game not found"}), 404

    return jsonify({"message": "game retrieved", "result": game_schema.dump(game_query)}), 200


@authenticate_return_auth
def update_game_by_id(request, game_id, auth_info):
    if auth_info.user.role != 'super-admin':
        return jsonify({"message": "unauthorized"}), 401

    post_data = request.form if request.form else request.json
    game_query = db.session.query(Game).filter(Game.game_id == game_id).first()

    if not game_query:
        return jsonify({"message": "game not found"}), 404

    populate_object(game_query, post_data)
    db.session.commit()

    return jsonify({"message": "game updated", "result": game_schema.dump(game_query)}), 200


@authenticate_return_auth
def delete_game(game_id, auth_info):
    if auth_info.user.role != 'super-admin':
        return jsonify({"message": "unauthorized"}), 401

    game = db.session.query(Game).filter(Game.game_id == game_id).first()

    if not game:
        return jsonify({"message": "game not found"}), 404

    try:
        db.session.delete(game)
        db.session.commit()
    except:
        db.session.rollback()
        return jsonify({"message": "error deleting game"}), 500

    return jsonify({"message": "game deleted"}), 200
