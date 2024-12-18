from flask import jsonify, request

from models.game import Game, game_schema, games_schema
from util.reflection import populate_object

from db import db


def add_game(request):
    post_data = request.form if request.form else request.json

    new_game = Game(
        date=post_data.get('date'),
        location=post_data.get('location'),
        home_team_id=post_data.get('home_team_id'),
        away_team_id=post_data.get('away_team_id')
    )
    populate_object(new_game, post_data)

    db.session.add(new_game)
    db.session.commit()

    return jsonify({"message": "game created", "result": game_schema.dump(new_game)}), 201


def get_all_games():
    games_query = db.session.query(Game).all()

    return jsonify({"message": "games retrieved", "result": games_schema.dump(games_query)}), 200


def get_game_by_id(game_id):
    game_query = db.session.query(Game).filter(Game.game_id == game_id).first()

    if not game_query:
        return jsonify({"message": "game not found"}), 404

    return jsonify({"message": "game retrieved", "result": game_schema.dump(game_query)}), 200


def update_game_by_id(request, game_id):
    post_data = request.form if request.form else request.json
    game_query = db.session.query(Game).filter(Game.game_id == game_id).first()

    if not game_query:
        return jsonify({"message": "game not found"}), 404

    populate_object(game_query, post_data)
    db.session.commit()

    return jsonify({"message": "game updated", "result": game_schema.dump(game_query)}), 200


def delete_game(game_id):
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
