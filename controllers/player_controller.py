from flask import jsonify, request

from models.player import Player, player_schema, players_schema
from util.reflection import populate_object

from db import db


def add_player(request):
    post_data = request.form if request.form else request.json

    name = post_data.get('name')
    existing_player = db.session.query(Player).filter(Player.name == name).first()

    if existing_player:
        return jsonify({"message": "player already exists"}), 400

    new_player = Player(
        name=post_data.get('name'),
        position=post_data.get('position'),
        team_id=post_data.get('team_id')
    )
    populate_object(new_player, post_data)

    db.session.add(new_player)
    db.session.commit()

    return jsonify({"message": "player created", "result": player_schema.dump(new_player)}), 201


def get_all_players():
    players_query = db.session.query(Player).all()

    return jsonify({"message": "players retrieved", "result": players_schema.dump(players_query)}), 200


def get_player_by_id(player_id):
    player_query = db.session.query(Player).filter(Player.player_id == player_id).first()

    if not player_query:
        return jsonify({"message": "player not found"}), 404

    return jsonify({"message": "player retrieved", "result": player_schema.dump(player_query)}), 200


def update_player_by_id(request, player_id):
    post_data = request.form if request.form else request.json
    player_query = db.session.query(Player).filter(Player.player_id == player_id).first()

    if not player_query:
        return jsonify({"message": "player not found"}), 404

    populate_object(player_query, post_data)
    db.session.commit()

    return jsonify({"message": "player updated", "result": player_schema.dump(player_query)}), 200


def delete_player(player_id):
    player = db.session.query(Player).filter(Player.player_id == player_id).first()

    if not player:
        return jsonify({"message": "player not found"}), 404

    try:
        db.session.delete(player)
        db.session.commit()
    except:
        db.session.rollback()
        return jsonify({"message": "error deleting player"}), 500

    return jsonify({"message": "player deleted"}), 200
