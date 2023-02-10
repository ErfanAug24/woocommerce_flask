from flask_marshmallow import Schema, Marshmallow
from marshmallow.validate import Length, Range
from marshmallow import validate, validates, validates_schema, Schema
from flask_marshmallow.fields import fields

from src.api_v2.models.user import UserModel
from src.api_v2.models.store import StoreModel

ma = Marshmallow()


class UserSchema(ma.SQLAlchemySchema):
    class Meta:
        model = UserModel

    id = fields.Str(required=True)
    username = fields.Str(required=True, validate=Length(255))
    email = fields.Str(required=True, validate=Length(255))
    password = fields.Str(required=True, validate=Length(255))

    @validates('username')
    def validate_username(self, value, **kwargs):
        if len(value) > 255:
            raise validate.ValidationError('the username length is out of standard number')

    @validates('email')
    def validate_email(self,value, **kwargs):
        pass

class UserValidation(UserSchema):
    pass


class StoreSchema(ma.SQLAlchemySchema):
    class Meta:
        model = StoreModel

    id = fields.Str(required=True)
    name = fields.Str(required=True, validate=Length(255))
    quantity = fields.Int(required=True)
    price = fields.Float(required=True)
