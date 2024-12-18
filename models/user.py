import uuid
from sqlalchemy.dialects.postgresql import UUID
import marshmallow as ma

from db import db


class User(db.Model):

    __tablename__ = "User"

    user_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    team_id = db.Column(UUID(as_uuid=True), db.ForeignKey("Team.team_id"), nullable=False)
    email = db.Column(db.String(), unique=True, nullable=False)
    password = db.Column(db.String(), nullable=False)

    def __init__(self, email, password):
        self.email = email
        self.password = password

    def new_user_obj():
        return User('', '')


class UserSchema(ma.Schema):
    class Meta:
        fields = ['user_id', 'team_id', 'email', 'password']


user_schema = UserSchema()
users_schema = UserSchema(many=True)
