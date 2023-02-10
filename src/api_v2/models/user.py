from src.db import db
from datetime import datetime


class UserModel(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=True, unique=True)
    email = db.Column(db.String(320), nullable=False, unique=True)
    password = db.Column(db.String, nullable=False, unique=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)
    stores = db.relationship('StoreModel', lazy='dynamic', backref='products')

    def __init__(self, username, email, password):
        self.username = username
        self.password = password
        self.email = email

    def json(self):
        return {'id': self.id, 'username': self.username, 'email': self.email, 'password': self.password,
                'created_at': "{}".format(self.created_at),
                'selected_stores': [x.json() for x in self.stores.all()]}

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
