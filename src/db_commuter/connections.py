# -*- coding: utf-8 -*-

"""
Connection to database
"""

import abc

import sqlite3
import psycopg2
from sqlalchemy import create_engine


__all__ = [
    "SQLiteConnection",
    "PgConnection"
]


class Connection(abc.ABC):
    """
    Abstract class, provides definitions of basic connection parameters
    """
    def __init__(self):
        """
        conn: connection to database
        engine: SQLAlchemy engine
        """
        self.conn = None
        self.engine = None

    def __del__(self):
        """
        close connection when class object is garbage collected
        """
        self.close_connection()
        self.close_engine()

    def get_conn(self):
        if self.conn is None:
            self.set_connection()
        return self.conn

    def get_engine(self):
        if self.engine is None:
            self.set_engine()
        return self.engine

    @abc.abstractmethod
    def set_connection(self, **kwargs):
        raise NotImplementedError()

    @abc.abstractmethod
    def set_engine(self, **kwargs):
        raise NotImplementedError()

    def close_connection(self):
        if self.conn is not None:
            self.conn.close()
            self.conn = None

    def close_engine(self):
        if self.engine is not None:
            self.engine.dispose()
            self.engine = None


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

    def set_engine(self, **kwargs):
        self.engine = create_engine('sqlite:///' + self.path2db, echo=False)


class PgConnection(Connection):
    """
    Establish connection with PostgreSQL database
    """
    def __init__(self, host, port, user, password, db_name, ssl_mode='prefer'):
        """
        :param db_name: name of database
        :param sslmode: mode of SSL TCP/IP connection
        """
        super().__init__()
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.db_name = db_name
        self.ssl_mode = ssl_mode

    def set_connection(self, **kwargs):
        """initialize connection using psycopg2.connect

        :param schema: if specified then schema is added to search_path in options
            parameter of connect.
        """
        schema = kwargs.get('schema', None)

        self.conn = psycopg2.connect(
            host=self.host,
            port=self.port,
            user=self.user,
            password=self.password,
            dbname=self.db_name,
            sslmode=self.ssl_mode,
            options=f'--search_path={schema}')

    def set_engine(self, **kwargs):
        engine = 'postgresql://' + self.user + ':' + self.password + '@' + \
            self.host + ':' + self.port + '/' + self.db_name + '?sslmode=' + self.ssl_mode
        self.engine = create_engine(engine)



