from typing import Dict, List, Union
from src.db import db
from datetime import datetime

StoreJSON = Dict[str, Union[int, str, float]]


class StoreModel(db.Model):
    __tablename__ = 'stores'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=True, unique=True)
    price = db.Column(db.Integer, nullable=False)
    quantity = db.Column(db.Integer, default=1)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __init__(self, name: str, price: int or float, user_id=int, quantity=int(1)):
        self.name = name
        self.price = price
        self.quantity = quantity
        self.user_id = user_id

    def json(self) -> StoreJSON:
        return {'id': self.id, 'name': self.name, 'price': self.price, 'quantity': self.quantity,
                'created time': "{}".format(self.created_at), 'user_id': self.user_id}

    @classmethod
    def find_by_name(cls, name: str) -> "StoreModel":
        return cls.query.filter_by(name=name).first()

    @classmethod
    def find_by_id(cls, _id: int) -> "StoreModel":
        return cls.query.filter_by(id=_id).first()

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()
