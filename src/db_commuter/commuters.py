# -*- coding: utf-8 -*-

"""
Collection of methods for communication with database
"""

import abc

from sqlalchemy import exc

from db_commuter.connections import *


class Commuter(abc.ABC):
    def __init__(self, connector):
        self.connector = connector

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

    def insert_from_pandas(self, table_name, data, **kwargs):
        """
        insert a pandas dataframe (data) into database table (table_name)

        :param chunksize: rows will be written in batches of this size at a time
        """
        chunksize = kwargs.get('chunksize', None)

        try:
            data.to_sql(table_name, con=self.connector.get_engine(),
                        if_exists='append', index=False, chunksize=chunksize)
        except (ValueError, exc.ProgrammingError) as error:
            return error

        self.connector.close_connection()

        return None


class SQLiteCommuter(Commuter):
    def __init__(self, path2db):
        super().__init__(SQLiteConnection(path2db))


class PgCommuter(Commuter):
    def __init__(self, host, port, user, password, db_name, ssl_mode):
        super().__init__(PgConnection(host, port, user, password, db_name, ssl_mode))
