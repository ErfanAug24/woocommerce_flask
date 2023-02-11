from marshmallow import Schema, fields


class UserSchema(Schema):
    class Meta:
        load_only = {"password", }  # your get method will just load the password not dumping it.
        dump_only = {"id", }

    id = fields.Int()
    username = fields.Str(required=True)
    email = fields.Email(required=True)
    password = fields.Str(required=True)
