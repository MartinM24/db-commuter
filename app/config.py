# -*- coding: utf-8 -*-

from os import path

root_dir = path.dirname(path.abspath(path.join(__file__, '..')))

# path to directory with .sql-scripts
path2scripts = path.join(root_dir, 'scripts')

# path to secret.env
path2env = path.join(root_dir, 'app', 'secret.env')

# path to SQLite database
path2sqlite = path.join(root_dir, 'db', 'test_db.sqlite3')