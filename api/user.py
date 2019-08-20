"""
User module used to create and enforce validation on our API inputs
"""
from dataclasses import dataclass
from marshmallow import Schema, fields, post_load


@dataclass
class User:
    """
    User object represents the user
    """

    user_id: int
    first_name: str
    last_name: str
    zip_code: str
    email_address: str


class UserSchema(Schema):
    """
    UserSchema object represents the validation of the
    User class
    Currently only data types are enforced and the email field must
    represent a valid email
    Postal code is string to include non-US zips
    (could add future validation if countries were known)
    """

    user_id = fields.Integer()
    first_name = fields.Str()
    last_name = fields.Str()
    email_address = fields.Email()
    zip_code = fields.Str()

    @post_load
    def make_user(self, data: dict, **kwargs):
        """
        Post-schema validation, returns a user object
        """
        return User(**data)
