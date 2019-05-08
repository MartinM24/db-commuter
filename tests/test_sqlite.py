# -*- coding: utf-8 -*-

"""
Test SQLite commuter methods
"""

from os import path

from datetime import datetime
import pandas as pd

from db_commuter.commuters import SQLiteCommuter
from app import config

commuter = SQLiteCommuter(config.path2sqlite)


def test_connection():
    assert commuter.connector.get_conn() is not None


def test_engine():
    assert commuter.connector.get_engine().connect().connection.is_valid


def test_execute():
    """
    execute 'create table' command and verify that table has been created
    """
    if commuter.is_table_exist('test_table'):
        commuter.delete_table('test_table')

    assert not commuter.is_table_exist('test_table')

    commuter.execute('create table if not exists test_table(var_a integer)')

    assert commuter.is_table_exist('test_table')

    commuter.delete_table('test_table')


def test_execute_script():
    """
    execute 'create table' command from .sql script and verify that table has been created
    """
    if commuter.is_table_exist('test_table'):
        commuter.delete_table('test_table')

    assert not commuter.is_table_exist('test_table')

    commuter.execute_script(path.join(config.path2scripts, 'create_test_table.sql'))

    assert commuter.is_table_exist('test_table')

    commuter.delete_table('test_table')


def test_select_insert(table_data):
    """
    insert from pandas dataframe to table and select from table to dataframe
    """
    if commuter.is_table_exist('test_table'):
        commuter.delete_table('test_table')

    commuter.execute_script(path.join(config.path2scripts, 'create_test_table.sql'))

    commuter.insert('test_table', table_data)

    data = commuter.select('select * from test_table')
    data['date'] = pd.to_datetime(data['var_a'])

    assert data['date'][0].date() == datetime.now().date()
    assert len(data) == 3

    commuter.delete_table('test_table')
