from api.user import User, UserSchema
from marshmallow import ValidationError
import pytest


schema = UserSchema()


def test_user_schema(snapshot):
    """
    Test the user schema with various cases
    (Schema validation comes from schema class)
    Snapshot test compares to previous run
    """
    valid_user = {
        "user_id": 123,
        "first_name": "Jack",
        "last_name": "Jones",
        "zip_code": "98683",
        "email_address": "jack@jones.biz",
    }
    actual = schema.dump(valid_user)
    snapshot.assert_match(actual)


def test_invalid_data():
    """
    Validation test
    """
    invalid_user = {
        "user_id": "string",
        "first_name": "Jack",
        "last_name": "Jones",
        "zip_code": "98683",
        "email_address": "jack@jones.biz",
    }
    with pytest.raises(ValueError):
        schema.dump(invalid_user)
