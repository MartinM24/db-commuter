# -*- coding: utf-8 -*-

"""
Test SQLite commuter methods
"""

from db_commuter import PgCommuter


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



