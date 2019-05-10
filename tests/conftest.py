# -*- coding: utf-8 -*-

"""
Test config
"""

import pytest

import numpy as np
import pandas as pd
from datetime import datetime

from db_commuter.commuters import *
import config


@pytest.fixture(scope='session')
def table_data():
    return pd.DataFrame({
        'var_1': pd.date_range(datetime.now(), periods=3),
        'var_2': [1, 2, 3],
        'var_3': ['x', 'xx', 'xxx'],
        'var_4': np.random.rand(3)
    })


@pytest.fixture(scope='session')
def sqlite_commuter():
    return SQLiteCommuter(config.path2sqlite)


@pytest.fixture(scope='session')
def pg_commuter():
    pg_config = config.postgres
    return PgCommuter(pg_config['localhost'], pg_config['port'],
                      pg_config['user'], pg_config['password'], pg_config['db_name'], False)


