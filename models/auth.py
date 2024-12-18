import uuid
from sqlalchemy.dialects.postgresql import UUID
import marshmallow as ma

from db import db


class Auth(db.Model):
    __tablename__ = "Auth"

    auth_token = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey("User.user_id"), nullable=False)
    expiration = db.Column(db.DateTime, nullable=False)

    def __init__(self, user_id, expiration):
        self.user_id = user_id
        self.expiration = expiration


class AuthSchema(ma.Schema):
    class Meta:
        fields = ['auth_token', 'user_id', 'expiration']


auth_schema = AuthSchema()
