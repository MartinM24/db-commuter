# -*- coding: utf-8 -*-

"""
Connection to database
"""

import abc

import sqlite3


__all__ = [
    "SQLiteConnection",
    "PgConnection"
]


class Connection(abc.ABC):
    """
    Abstract class, provides definitions of basic connection parameters
    """
    def __init__(self):
        self.conn = None

    def __del__(self):
        """
        close connection when class object is garbage collected
        """
        self.close_connection()

    def get_conn(self):
        if self.conn is None:
            self.set_connection()
        return self.conn

    @abc.abstractmethod
    def set_connection(self, **kwargs):
        raise NotImplementedError()

    @abc.abstractmethod
    def close_connection(self):
        raise NotImplementedError()


class SQLiteConnection(Connection):
    """
    Establish connection with SQLite database
    """
    def __init__(self, path2db):
        """
        :param path2db: path to database file
        """
        super().__init__()
        self.path2db = path2db

    def set_connection(self):
        self.conn = sqlite3.connect(self.path2db)

    def close_connection(self):
        self.conn.close()


class PgConnection(Connection):
    """
    Establish connection with PostgreSQL database
    """
    def __init__(self, host, port, user, password, db_name, ssl_mode):
        """
        :param db_name: name of database
        :param ssl_mode: boolean
        """
        super().__init__()
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.db_name = db_name
        self.ssl_mode = ssl_mode

    def set_connection(self, **kwargs):
        raise NotImplementedError()

    def close_connection(self):
        raise NotImplementedError
