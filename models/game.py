import uuid
from sqlalchemy.dialects.postgresql import UUID
import marshmallow as ma

from db import db


class Game(db.Model):
    __tablename__ = "Game"

    game_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    date = db.Column(db.Date, nullable=False)
    location = db.Column(db.String, nullable=False)
    home_team_id = db.Column(UUID(as_uuid=True), db.ForeignKey("Team.team_id"), nullable=False)
    away_team_id = db.Column(UUID(as_uuid=True), db.ForeignKey("Team.team_id"), nullable=False)

    home_team = db.relationship("Team", foreign_keys=[home_team_id], back_populates="home_games")
    away_team = db.relationship("Team", foreign_keys=[away_team_id], back_populates="away_games")

    def __init__(self, date, location, home_team_id, away_team_id):
        self.date = date
        self.location = location
        self.home_team_id = home_team_id
        self.away_team_id = away_team_id


class GameSchema(ma.Schema):
    class Meta:
        fields = ['game_id', 'date', 'location', 'home_team', 'away_team']
    home_team = ma.fields.Nested("TeamSchema", exclude=['home_games', 'away_games'])
    away_team = ma.fields.Nested("TeamSchema", exclude=['home_games', 'away_games'])


game_schema = GameSchema()
games_schema = GameSchema(many=True)
