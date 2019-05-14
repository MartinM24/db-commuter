# Database Communication Manager

Collection of methods for communication with database. Supports following databases: 

* SQLite
* PostgreSQL

## Installation

To install the package, simply use pip.

```
$ pip install db_commuter
```

## SQLite

To initialize SQLite communication agent, you need to pass path to database file to constructor.

```python
from db_commuter.commuters import SQLiteCommuter
commuter = SQLiteCommuter(path2db)
```

Basic operations on database tables.

```python
# insert from pandas dataframe to table
commuter.insert(table_name, data)
# select from table to pandas dataframe
data = commuter.select('select * from table_name')
# delete table
commuter.delete_table('test_table') 
```

## PostgreSQL

```python
from db_commuter.commuters import PgCommuter
commuter = PgCommuter(host, port, user, password, db_name, ssl_mode)

# alternative method using dictionary contained required connection parameters
params = {'host': 'localhost', 'port': '5432', 'user': 'postgres', 
    'password': 'password', 'db_name': 'test_db', 'ssl_mode': False}
commuter = PgCommuter.from_dict(params) 
```

## License

Package is released under [MIT License](https://github.com/viktorsapozhok/db-commuter/blob/master/LICENSE).





