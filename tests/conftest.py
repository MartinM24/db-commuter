# -*- coding: utf-8 -*-

"""
Test config
"""

import pytest
from os import path

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
    return PgCommuter.from_dict(pg_config)


@pytest.fixture(scope='session')
def testers():
    return Testers


class Testers:
    @staticmethod
    def test_connection(commuter):
        assert commuter.connector.get_conn() is not None

    @staticmethod
    def test_engine(commuter):
        assert commuter.connector.get_engine().connect().connection.is_valid

    @staticmethod
    def test_execute(commuter):
        if commuter.is_table_exist('test_table'):
            commuter.delete_table('test_table')

        assert not commuter.is_table_exist('test_table')

        commuter.execute('create table if not exists test_table(var_a integer)')

        assert commuter.is_table_exist('test_table')

        commuter.delete_table('test_table')

    @staticmethod
    def test_execute_script(commuter):
        """
        execute 'create table' command from .sql script and verify that table has been created
        """
        if commuter.is_table_exist('test_table'):
            commuter.delete_table('test_table')

        assert not commuter.is_table_exist('test_table')

        commuter.execute_script(path.join(config.path2scripts, 'create_test_table.sql'))

        assert commuter.is_table_exist('test_table')

        commuter.delete_table('test_table')

    @staticmethod
    def test_select_insert(commuter, table_data):
        """
        insert from pandas dataframe to table and select from table to dataframe
        """
        if commuter.is_table_exist('test_table'):
            commuter.delete_table('test_table')

        commuter.execute_script(path.join(config.path2scripts, 'create_test_table.sql'))

        commuter.insert('test_table', table_data)

        data = commuter.select('select * from test_table')
        data['date'] = pd.to_datetime(data['var_1'])

        assert data['date'][0].date() == datetime.now().date()
        assert len(data) == 3

        commuter.delete_table('test_table')


