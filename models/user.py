import uuid
from sqlalchemy.dialects.postgresql import UUID
import marshmallow as ma

from db import db


class User(db.Model):

    __tablename__ = "User"

    user_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    first_name = db.Column(db.String(), nullable=False)
    last_name = db.Column(db.String(), nullable=False)
    email = db.Column(db.String(), unique=True, nullable=False)
    password = db.Column(db.String(), nullable=False)
    role = db.Column(db.String(), nullable=False)

    auth = db.relationship("Auth", back_populates="user")

    def __init__(self, first_name, last_name, email, password, role):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password
        self.role = role

    def new_user_obj():
        return User('', '', '', '', '')


class UserSchema(ma.Schema):
    class Meta:
        fields = ['user_id', 'first_name', 'last_name', 'email', 'role']


user_schema = UserSchema()
users_schema = UserSchema(many=True)
