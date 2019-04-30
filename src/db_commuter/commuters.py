# -*- coding: utf-8 -*-

"""
Collection of methods for communication with database
"""

from db_commuter.connections import *


class SQLiteCommuter(object):
    def __init__(self, path2db):
        self.connector = SQLiteConnection(path2db)

    def execute(self, cmd, commit=True):
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
        conn.close()

