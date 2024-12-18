import uuid
from sqlalchemy.dialects.postgresql import UUID
import marshmallow as ma

from db import db


class Player(db.Model):
    __tablename__ = "Player"

    player_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = db.Column(db.String, nullable=False)
    position = db.Column(db.String, nullable=False)
    team_id = db.Column(UUID(as_uuid=True), db.ForeignKey("Team.team_id"), nullable=False)

    team = db.relationship("Team", back_populates="players")

    def __init__(self, name, position, team_id):
        self.name = name
        self.position = position
        self.team_id = team_id


class PlayerSchema(ma.Schema):
    class Meta:
        fields = ['player_id', 'name', 'position', 'team']

    team = ma.fields.Nested("TeamSchema", exclude=['players'])


player_schema = PlayerSchema()
players_schema = PlayerSchema(many=True)
