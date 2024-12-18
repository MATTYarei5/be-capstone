from flask import jsonify, request
from flask_bcrypt import generate_password_hash

from models.user import User, user_schema, users_schema
from util.reflection import populate_object
from lib.authenticate import auth

from db import db


def add_user(request):
    post_data = request.form if request.form else request.json

    email = post_data.get('email')
    existing_user = db.session.query(User).filter(User.email == email).first()

    if existing_user:
        return jsonify({"message": "user already exists"}), 400

    new_user = User.new_user_obj()
    populate_object(new_user, post_data)
    new_user.password = generate_password_hash(new_user.password).decode('utf-8')

    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "user created", "result": user_schema.dump(new_user)}), 201


@auth
def get_all_users():
    users_query = db.session.query(User).all()

    return jsonify({"message": "users retrieved", "result": users_schema.dump(users_query)}), 200


@auth
def get_user_by_id(user_id):
    user_query = db.session.query(User).filter(User.user_id == user_id).first()

    if not user_query:
        return jsonify({"message": "user not found"}), 404

    return jsonify({"message": "user retrieved", "result": user_schema.dump(user_query)}), 200


@auth
def update_user_by_id(request, user_id):
    post_data = request.form if request.form else request.json
    user_query = db.session.query(User).filter(User.user_id == user_id).first()

    if not user_query:
        return jsonify({"message": "user not found"}), 404

    populate_object(user_query, post_data)
    db.session.commit()

    return jsonify({"message": "user updated", "result": user_schema.dump(user_query)}), 200


@auth
def delete_user(user_id):
    user = db.session.query(User).filter(User.user_id == user_id).first()

    if not user:
        return jsonify({"message": "user not found"}), 404

    try:
        db.session.delete(user)
        db.session.commit()
    except:
        db.session.rollback()
        return jsonify({"message": "unable to delete user"}), 500

    return jsonify({"message": "user deleted"}), 200
