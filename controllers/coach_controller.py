from flask import jsonify, request

from models.coach import Coach, coach_schema, coaches_schema
from util.reflection import populate_object
from lib.authenticate import authenticate_return_auth, auth

from db import db


@authenticate_return_auth
def add_coach(request, auth_info):
    if auth_info.user.role != 'super-admin':
        return jsonify({"message": "unauthorized"}), 401

    post_data = request.form if request.form else request.json

    name = post_data.get('name')
    existing_coach = db.session.query(Coach).filter(Coach.name == name).first()

    if existing_coach:
        return jsonify({"message": "coach already exists"}), 400

    new_coach = Coach(name=post_data.get('name'), experience=post_data.get('experience'))
    populate_object(new_coach, post_data)

    db.session.add(new_coach)
    db.session.commit()

    return jsonify({"message": "coach created", "result": coach_schema.dump(new_coach)}), 201


@auth
def get_all_coaches(request):
    coaches_query = db.session.query(Coach).all()

    return jsonify({"message": "coaches retrieved", "result": coaches_schema.dump(coaches_query)}), 200


@auth
def get_coach_by_id(coach_id):
    coach_query = db.session.query(Coach).filter(Coach.coach_id == coach_id).first()

    if not coach_query:
        return jsonify({"message": "coach not found"}), 404

    return jsonify({"message": "coach retrieved", "result": coach_schema.dump(coach_query)}), 200


@authenticate_return_auth
def update_coach_by_id(request, coach_id, auth_info):
    if auth_info.user.role != 'super-admin':
        return jsonify({"message": "unauthorized"}), 401

    post_data = request.form if request.form else request.json

    coach_query = db.session.query(Coach).filter(Coach.coach_id == coach_id).first()

    if not coach_query:
        return jsonify({"message": "coach not found"}), 404

    populate_object(coach_query, post_data)
    db.session.commit()

    return jsonify({"message": "coach updated", "result": coach_schema.dump(coach_query)}), 200


@authenticate_return_auth
def delete_coach(coach_id, auth_info):

    if auth_info.user.role != 'super-admin':
        return jsonify({"message": "unauthorized"}), 401

    coach = db.session.query(Coach).filter(Coach.coach_id == coach_id).first()

    if not coach:
        return jsonify({"message": "coach not found"}), 404

    try:
        db.session.delete(coach)
        db.session.commit()
    except:
        db.session.rollback()
        return jsonify({"message": "error deleting coach"}), 500

    return jsonify({"message": "coach deleted"}), 200
