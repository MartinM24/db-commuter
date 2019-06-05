# -*- coding: utf-8 -*-

"""Test SQLite commuter methods
"""

from os import path

import pandas as pd
from datetime import datetime

from db_commuter import PgCommuter
import config


def test_connection(pg_commuter, testers):
    testers.test_connection((pg_commuter))


def test_connection_keywords(testers):
    commuter = PgCommuter(
        'localhost', '5432', 'postgres', 'password', 'test_db',
        sslmode='require', schema='public')
    testers.test_connection(commuter)


def test_engine(pg_commuter, testers):
    testers.test_engine(pg_commuter)


def test_engine_keywords(testers):
    commuter = PgCommuter(
        'localhost', '5432', 'postgres', 'password', 'test_db',
        sslmode='require', schema='public')
    testers.test_engine(commuter)


def test_execute(pg_commuter, testers):
    testers.test_execute(pg_commuter)


def test_execute_script(pg_commuter, testers):
    testers.test_execute_script(pg_commuter)


def test_select_insert(pg_commuter, table_data, testers):
    testers.test_select_insert(pg_commuter, table_data)


def test_insert_fast(pg_commuter, table_data):
    if pg_commuter.is_table_exist('test_table'):
        pg_commuter.delete_table('test_table')

    pg_commuter.execute_script(path.join(config.path2scripts, 'create_test_table.sql'))

    pg_commuter.insert_fast('test_table', table_data)

    data = pg_commuter.select('select * from test_table')
    data['date'] = pd.to_datetime(data['var_1'])

    assert data['date'][0].date() == datetime.now().date()
    assert len(data) == 3

    pg_commuter.delete_table('test_table')


def test_execute_with_params(pg_commuter):
    if pg_commuter.is_table_exist('people'):
        pg_commuter.delete_table('people')

    who = "Yeltsin"
    age = 72

    pg_commuter.execute("create table if not exists people(name_last text, age integer)")
    pg_commuter.execute("insert into people values (%s, %s)", vars=(who, age))

    data = pg_commuter.select('select * from people')
    assert data['age'][0] == 72
    assert len(data) == 1

    pg_commuter.delete_table('people')


def test_schema(testers, table_data):
    commuter = PgCommuter(
        'localhost', '5432', 'postgres', 'password', 'test_db',
        schema='model')

    testers.test_select_insert(commuter, table_data)

