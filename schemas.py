from marshmallow import Schema, fields

# Using the marshmallow library for data validation, using these schemas to pass them into the endpoints so that when
# payloads come in from the user the data received is of the correct type.

class PlainUserSchema(Schema):
    id = fields.Int(dump_only=True)
    username = fields.Str(required=True)
    password = fields.Str(required=True, load_only=True)

class PLainURLSchema(Schema):
    id = fields.Int(dump_only=True)
    original_url = fields.Str(required=True)
    user_id = fields.Int(required=True)
    short_url = fields.Str(required=True)
    searchable_short_url = fields.Str(required=True)
    custom_url = fields.Str(allow_none=True, missing=None)

# Using this schema will populate a list with all the URLS that correlate with the user_id attached to the url.
class UserSchema(PlainUserSchema):
    url_info = fields.List(fields.Nested(PLainURLSchema()), dump_only=True)