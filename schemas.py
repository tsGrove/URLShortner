from marshmallow import Schema, fields

class PlainUserSchema(Schema):
    id = fields.Int(dump_only=True)
    username = fields.Str(required=True)
    password = fields.Str(required=True, load_only=True)

class PLainURLSchema(Schema):
    id = fields.Int(dump_only=True)
    original_url = fields.Str(required=True)
    user_id = fields.Int(required=True)
    short_url = fields.Str(required=True)
    custom_url = fields.Str()

class UserSchema(PlainUserSchema):
    short_url = fields.List(fields.Nested(PLainURLSchema()), dump_only=True)