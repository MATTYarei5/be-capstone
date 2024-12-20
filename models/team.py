import uuid
from sqlalchemy.dialects.postgresql import UUID
import marshmallow as ma

from db import db
from models.team_game_xref import team_game_xref_table


class Team(db.Model):
    __tablename__ = "Team"

    team_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = db.Column(db.String, nullable=False)
    coach_id = db.Column(UUID(as_uuid=True), db.ForeignKey("Coach.coach_id"), nullable=False)

    coach = db.relationship("Coach", back_populates="teams")
    players = db.relationship("Player", back_populates="team")
    games = db.relationship("Game", secondary=team_game_xref_table, back_populates="teams")

    def __init__(self, name, coach_id):
        self.name = name
        self.coach_id = coach_id


class TeamSchema(ma.Schema):
    class Meta:
        fields = ['team_id', 'name', 'coach', 'players', 'games']

    coach = ma.fields.Nested("CoachSchema", exclude=['teams'])
    players = ma.fields.Nested("PlayerSchema", many=True, exclude=['team'])
    games = ma.fields.Nested("GameSchema", many=True, exclude=['teams'])


team_schema = TeamSchema()
teams_schema = TeamSchema(many=True)
