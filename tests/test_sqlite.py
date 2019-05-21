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


def test_execute_with_params(sqlite_commuter):
    who = "Yeltsin"
    age = 72

    sqlite_commuter.execute("create table if not exists people(name_last, age)")
    sqlite_commuter.execute("insert into people values (?, ?)", vars=(who, age))

    data = sqlite_commuter.select('select * from people')
    assert data['age'][0] == 72
    assert len(data) == 1

    sqlite_commuter.delete_table('people')


