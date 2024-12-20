import uuid
from sqlalchemy.dialects.postgresql import UUID
import marshmallow as ma

from db import db
from models.team_game_xref import team_game_xref_table


class Game(db.Model):
    __tablename__ = "Game"

    game_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    date = db.Column(db.Date, nullable=False)
    location = db.Column(db.String, nullable=False)

    teams = db.relationship("Team", secondary=team_game_xref_table, back_populates="games")

    def __init__(self, date, location):
        self.date = date
        self.location = location

    def new_game_obj():
        return Game('', '')


class GameSchema(ma.Schema):
    class Meta:
        fields = ['game_id', 'date', 'location', 'teams']

    teams = ma.fields.Nested("TeamSchema", many=True, exclude=['games'])


game_schema = GameSchema()
games_schema = GameSchema(many=True)
