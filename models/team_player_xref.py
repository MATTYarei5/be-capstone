from db import db

team_player_xref_table = db.Table(
    "TeamPlayerXref",
    db.Model.metadata,
    db.Column("player_id", db.ForeignKey("Player.player_id", ondelete='CASCADE'), primary_key=True),
    db.Column("team_id", db.ForeignKey("Team.team_id", ondelete='CASCADE'), primary_key=True)
)
