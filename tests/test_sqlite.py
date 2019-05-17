# -*- coding: utf-8 -*-

"""
Test SQLite commuter methods
"""

def test_connection(sqlite_commuter, testers):
    testers.test_connection(sqlite_commuter)


def test_engine(sqlite_commuter, testers):
    testers.test_engine(sqlite_commuter)


def test_execute(sqlite_commuter, testers):
    testers.test_execute(sqlite_commuter)


def test_execute_script(sqlite_commuter, testers):
    testers.test_execute_script(sqlite_commuter)


def test_select_insert(sqlite_commuter, table_data, testers):
    testers.test_select_insert(sqlite_commuter, table_data)
