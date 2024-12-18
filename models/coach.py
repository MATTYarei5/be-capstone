import uuid
from sqlalchemy.dialects.postgresql import UUID
import marshmallow as ma

from db import db


class Coach(db.Model):
    __tablename__ = "Coach"

    coach_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = db.Column(db.String, nullable=False)
    experience = db.Column(db.Integer, nullable=False)

    teams = db.relationship("Team", back_populates="coach")

    def __init__(self, name, experience):
        self.name = name
        self.experience = experience


class CoachSchema(ma.Schema):
    class Meta:
        fields = ['coach_id', 'name', 'experience', 'teams']
    teams = ma.fields.Nested("TeamSchema", many=True, exclude=['coach'])


coach_schema = CoachSchema()
coaches_schema = CoachSchema(many=True)
