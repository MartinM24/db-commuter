# -*- coding: utf-8 -*-

"""
Test config
"""

import pytest
from os import getenv

from dotenv import load_dotenv

from db_commuter.commuters import *
from app import config

load_dotenv(config.path2env)


@pytest.fixture(scope='session')
def sqlite_commuter():
    return SQLiteCommuter(getenv('PATH_TO_SQLITE_DB'))

@pytest.fixture(scope='session')
def pg_commuter():
    host = getenv('PG_TEST_DB_HOST')
    port = getenv('PG_TEST_DB_PORT')
    user = getenv('PG_TEST_DB_USER')
    password = getenv('PG_TEST_DB_PASS')
    db_name = getenv('PG_TEST_DB_NAME')

    return PgCommuter(host, port, user, password, db_name, False)
