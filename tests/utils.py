# -*- coding: utf-8 -*-

"""
Testing utilities
"""


def test_connection(commuter):
    assert commuter.connector.get_conn() is not None


def test_engine(commuter):
    assert commuter.connector.get_engine().connect().connection.is_valid
