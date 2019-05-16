# -*- coding: utf-8 -*-

from os import path

root_dir = path.dirname(path.abspath(__file__))

# path to directory with .sql-scripts
path2scripts = path.join(root_dir, 'scripts')

# path to SQLite database
path2sqlite = path.join(root_dir, 'db', 'test_db.sqlite3')

# PostgreSQL access parameters
postgres = {
    'host': 'localhost',
    'port': '5432',
    'user': 'postgres',
    'password': 'password',
    'db_name': 'test_db'
}