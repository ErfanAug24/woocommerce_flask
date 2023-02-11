from src.db import db
from typing import Dict, List, Union
from datetime import datetime

BlacklistJSON = Dict[str, str]


class User_BlackList(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    jwt_id = db.Column(db.String, nullable=False, unique=True)
    revoked_at = db.Column(db.DateTime, default=datetime.utcnow)
    reason = db.Column(db.String(255), nullable=False)

    def __init__(self, jwt_id, reason):
        self.jwt_id = jwt_id
        self.reason = reason

    def json(self) -> BlacklistJSON:
        return {'id': self.id,
                'jwt_id': self.jwt_id,
                'revoked_at': "{}".format(self.revoked_at),
                'reason': self.reason}

    @classmethod
    def find_by_id(cls, _id) -> "User_BlackList":
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def find_by_jwt_id(cls, jwt_id) -> "User_BlackList":
        return cls.query.filter_by(jwt_id=jwt_id).first()

    @classmethod
    def find_all(cls) -> "User_BlackList":
        return cls.query.all()

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()
