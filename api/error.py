"""
Errors module represents the format of error and the types
used for our API.
"""


def UserAlreadyExistsError(user_id: int):
    """Error happens when trying to create a user that already exists"""
    result = {
        "message": f"A user with user_id {user_id} already exists.",
        "status": 409,
    }
    return result


def ResourceDoesNotExist(user_id: int):
    """Error happens when trying to access a user that doesn't exist"""
    result = {
        "message": f"A user with user_id {user_id} does not exist.",
        "status": 410,
    }
    return result


def SchemaValidationError(user_id: int, validation_message):
    """
    Error happens when trying to create a user without necessary attributes
    or when attributes are incorrect data types
    """
    result = {
        "message": f"Validation error processing record for user: {user_id}.",
        "status": 422,
        "extra": validation_message,
    }
    return result
