# -*- coding: utf-8 -*-

"""
Test SQLite commuter methods
"""

from os import path

from datetime import datetime
import pandas as pd

import config


def test_connection(sqlite_commuter):
    assert sqlite_commuter.connector.get_conn() is not None


def test_engine(sqlite_commuter):
    assert sqlite_commuter.connector.get_engine().connect().connection.is_valid


def test_execute(sqlite_commuter):
    """
    execute 'create table' command and verify that table has been created
    """
    if sqlite_commuter.is_table_exist('test_table'):
        sqlite_commuter.delete_table('test_table')

    assert not sqlite_commuter.is_table_exist('test_table')

    sqlite_commuter.execute('create table if not exists test_table(var_a integer)')

    assert sqlite_commuter.is_table_exist('test_table')

    sqlite_commuter.delete_table('test_table')


def test_execute_script(sqlite_commuter):
    """
    execute 'create table' command from .sql script and verify that table has been created
    """
    if sqlite_commuter.is_table_exist('test_table'):
        sqlite_commuter.delete_table('test_table')

    assert not sqlite_commuter.is_table_exist('test_table')

    sqlite_commuter.execute_script(path.join(config.path2scripts, 'create_test_table.sql'))

    assert sqlite_commuter.is_table_exist('test_table')

    sqlite_commuter.delete_table('test_table')


def test_select_insert(sqlite_commuter, table_data):
    """
    insert from pandas dataframe to table and select from table to dataframe
    """
    if sqlite_commuter.is_table_exist('test_table'):
        sqlite_commuter.delete_table('test_table')

    sqlite_commuter.execute_script(path.join(config.path2scripts, 'create_test_table.sql'))

    sqlite_commuter.insert('test_table', table_data)

    data = sqlite_commuter.select('select * from test_table')
    data['date'] = pd.to_datetime(data['var_1'])

    assert data['date'][0].date() == datetime.now().date()
    assert len(data) == 3

    sqlite_commuter.delete_table('test_table')
