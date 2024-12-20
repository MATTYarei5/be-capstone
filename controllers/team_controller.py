from flask import jsonify, request

from models.team import Team, team_schema, teams_schema
from util.reflection import populate_object
from lib.authenticate import authenticate_return_auth, auth

from db import db


@authenticate_return_auth
def add_team(request, auth_info):
    if auth_info.user.role != 'super-admin':
        return jsonify({"message": "unauthorized"}), 401

    post_data = request.form if request.form else request.json

    name = post_data.get('name')
    existing_team = db.session.query(Team).filter(Team.name == name).first()

    if existing_team:
        return jsonify({"message": "team already exists"}), 400

    new_team = Team(
        name=post_data.get('name'),
        coach_id=post_data.get('coach_id')
    )
    populate_object(new_team, post_data)

    db.session.add(new_team)
    db.session.commit()

    return jsonify({"message": "team created", "result": team_schema.dump(new_team)}), 201


@auth
def get_all_teams():
    teams_query = db.session.query(Team).all()

    return jsonify({"message": "teams retrieved", "result": teams_schema.dump(teams_query)}), 200


@auth
def get_team_by_id(team_id):
    team_query = db.session.query(Team).filter(Team.team_id == team_id).first()

    if not team_query:
        return jsonify({"message": "team not found"}), 404

    return jsonify({"message": "team retrieved", "result": team_schema.dump(team_query)}), 200


@authenticate_return_auth
def update_team_by_id(request, team_id, auth_info):
    if auth_info.user.role != 'super-admin':
        return jsonify({"message": "unauthorized"}), 401

    post_data = request.form if request.form else request.json
    team_query = db.session.query(Team).filter(Team.team_id == team_id).first()

    if not team_query:
        return jsonify({"message": "team not found"}), 404

    populate_object(team_query, post_data)
    db.session.commit()

    return jsonify({"message": "team updated", "result": team_schema.dump(team_query)}), 200


@authenticate_return_auth
def delete_team(team_id, auth_info):
    if auth_info.user.role != 'super-admin':
        return jsonify({"message": "unauthorized"}), 401

    team = db.session.query(Team).filter(Team.team_id == team_id).first()

    if not team:
        return jsonify({"message": "team not found"}), 404

    try:
        db.session.delete(team)
        db.session.commit()
    except:
        db.session.rollback()
        return jsonify({"message": "error deleting team"}), 500

    return jsonify({"message": "team deleted"}), 200
