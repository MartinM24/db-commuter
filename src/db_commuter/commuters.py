# -*- coding: utf-8 -*-

"""
Collection of methods for communication with database
"""

import abc

import pandas as pd

from db_commuter.connections import *

__all__ = [
    "SQLiteCommuter",
    "PgCommuter"
]


class Commuter(abc.ABC):
    def __init__(self, connector):
        self.connector = connector

    @abc.abstractmethod
    def select(self, cmd, **kwargs):
        """
        select data from database object using selection command (cmd)
        and put it in pandas object
        """
        raise NotImplementedError()

    @abc.abstractmethod
    def insert(self, obj, data, **kwargs):
        """
        insert pandas object (data) into database object (obj)
        """
        raise NotImplementedError()


class SQLCommuter(Commuter):
    """
    Parent class for SQL databases
    """
    def __init__(self, connector):
        super().__init__(connector)

    def delete_table(self, table_name, **kwargs):
        raise NotImplementedError()

    def is_table_exist(self, table_name, **kwargs):
        raise NotImplementedError()

    def execute(self, cmd, commit=True):
        """
        execute SQL command (cmd) and commit (if True) changes to database
        """
        # set the connection
        conn = self.connector.get_conn()
        # create cursor object
        cur = conn.cursor()
        # execute sql command
        cur.execute(cmd)

        # save the changes
        if commit:
            conn.commit()

        # close the connection
        self.connector.close_connection()

    def execute_script(self, path2script, commit=True):
        """
        execute multiple SQL statements separated by semicolon
        """
        with open(path2script, 'r') as fh:
            script = fh.read()

        conn = self.connector.get_conn()
        cur = conn.cursor()
        cur.executescript(script)

        if commit:
            conn.commit()

        self.connector.close_connection()

    def select(self, cmd, **kwargs):
        with self.connector.get_engine().connect() as conn:
            data = pd.read_sql_query(cmd, conn)

        self.connector.close_engine()

        return data

    def insert(self, table_name, data, **kwargs):
        """
        insert pandas dataframe (data) into database table (table_name)

        :param schema: specify the schema, if None, use default schema.
        :param chunksize: rows will be written in batches of this size at a time
        """
        schema = kwargs.get('schema', None)
        chunksize = kwargs.get('chunksize', None)

        data.to_sql(table_name, con=self.connector.get_engine(),
                    schema=schema, if_exists='append', index=False, chunksize=chunksize)

        self.connector.close_engine()


class SQLiteCommuter(SQLCommuter):
    """
    Methods for communication with SQLite database
    """
    def __init__(self, path2db):
        super().__init__(SQLiteConnection(path2db))

    def delete_table(self, table_name, **kwargs):
        self.execute('drop table if exists %s' % table_name)

    def is_table_exist(self, table_name, **kwargs):
        cmd = 'select name from sqlite_master where type=\'table\' and name=\'%s\'' % table_name

        data = self.select(cmd)

        if len(data) > 0:
            return data.name[0] == table_name

        return False


class PgCommuter(SQLCommuter):
    """
    Methods for communication with PostgreSQL database
    """
    def __init__(self, host, port, user, password, db_name, ssl_mode):
        super().__init__(PgConnection(host, port, user, password, db_name, ssl_mode))

    @classmethod
    def from_dict(cls, params):
        """alternative constructor used access parameters from dictionary
        """
        return cls(params['host'], params['port'], params['user'],
                   params['password'], params['db_name'], params['ssl_mode'])

    def delete_table(self, table_name, **kwargs):
        """
        :param schema: name of the database schema
        :param cascade: boolean, True if delete cascade
        """
        schema = kwargs.get('schema', None)
        cascade = kwargs.get('cascade', False)

        table_name = self.__get_table_name(schema, table_name)

        if cascade:
            self.execute('drop table if exists %s cascade' % table_name)
        else:
            self.execute('drop table if exists %s' % table_name)

    def is_table_exist(self, table_name, **kwargs):
        schema = kwargs.get('schema', None)

        table_name = self.__get_table_name(schema, table_name)

        raise NotImplementedError()

    @staticmethod
    def __get_table_name(schema, table_name):
        if schema is None:
            return table_name
        return schema + '.' + table_name
