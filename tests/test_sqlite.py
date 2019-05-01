# -*- coding: utf-8 -*-

"""
Test SQLite commuter methods
"""

from db_commuter.commuters import SQLiteCommuter
from app import config

commuter = SQLiteCommuter(config.path2sqlite)


def test_connection():
    assert commuter.connector.get_conn() is not None


def test_engine():
    assert commuter.connector.get_engine().connect().connection.is_valid


def test_execute():
    if commuter.is_table_exist('test_table'):
        commuter.delete_table('test_table')

    assert not commuter.is_table_exist('test_table')

    commuter.execute('create table if not exists test_table(var_a integer)')

    assert commuter.is_table_exist('test_table')

    commuter.delete_table('test_table')
