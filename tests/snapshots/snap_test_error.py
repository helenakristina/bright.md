# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots["test_resource_does_not_exist 1"] = {
    "message": "A user with user_id 123 does not exist.",
    "status": 410,
}

snapshots["test_user_exists 1"] = {
    "message": "A user with user_id 123 already exists.",
    "status": 409,
}

snapshots["test_invalid_schema 1"] = {
    "extra": "Schema does not validate",
    "message": "Validation error processing record for user: 123.",
    "status": 422,
}
