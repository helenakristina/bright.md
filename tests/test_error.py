"""
Snapshot tests for error output
"""

from api.error import (
    UserAlreadyExistsError,
    ResourceDoesNotExist,
    SchemaValidationError,
)


def test_user_exists(snapshot):
    user_id = 123
    actual = UserAlreadyExistsError(user_id)
    snapshot.assert_match(actual)


def test_resource_does_not_exist(snapshot):
    user_id = 123
    actual = ResourceDoesNotExist(user_id)
    snapshot.assert_match(actual)


def test_invalid_schema(snapshot):
    user_id = 123
    message = "Schema does not validate"
    actual = SchemaValidationError(user_id, message)
    snapshot.assert_match(actual)
