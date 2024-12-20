from db import db

team_game_xref_table = db.Table(
    "TeamGameXref",
    db.Model.metadata,
    db.Column("game_id", db.ForeignKey("Game.game_id", ondelete='CASCADE'), primary_key=True),
    db.Column("team_id", db.ForeignKey("Team.team_id", ondelete='CASCADE'), primary_key=True)
)
