# -*- coding: utf-8 -*-

"""
Test config
"""

import pytest
from os import getenv

from dotenv import load_dotenv

import numpy as np
import pandas as pd
from datetime import datetime

from db_commuter.commuters import *
from app import config

load_dotenv(config.path2env)


@pytest.fixture(scope='session')
def table_data():
    return pd.DataFrame({
        'var_a': pd.date_range(datetime.now(), periods=3),
        'var_b': [1, 2, 3],
        'var_c': ['x', 'xx', 'xxx'],
        'var_d': np.random.rand(3)
    })


@pytest.fixture(scope='session')
def pg_commuter():
    host = getenv('PG_TEST_DB_HOST')
    port = getenv('PG_TEST_DB_PORT')
    user = getenv('PG_TEST_DB_USER')
    password = getenv('PG_TEST_DB_PASS')
    db_name = getenv('PG_TEST_DB_NAME')

    return PgCommuter(host, port, user, password, db_name, False)


