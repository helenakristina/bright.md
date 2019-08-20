# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots["test_user_schema 1"] = {
    "email_address": "jack@jones.biz",
    "first_name": "Jack",
    "last_name": "Jones",
    "user_id": 123,
    "zip_code": "98683",
}
