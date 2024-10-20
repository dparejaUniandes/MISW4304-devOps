from datetime import datetime

from flask_sqlalchemy import SQLAlchemy
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from sqlalchemy.dialects.postgresql import UUID

db = SQLAlchemy()

class Blacklist(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String, nullable=False, unique=True)
    app_uuid = db.Column(UUID(as_uuid=True), unique=True)
    blocked_reason = db.Column(db.String(255), nullable=False)
    ip_address = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)

class BlacklistSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Blacklist
        load_instance = True
        exclude = ('id', 'ip_address', 'created_at')
