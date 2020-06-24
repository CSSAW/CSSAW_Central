# CSSAW_Central

## Installation
``` Bash
pip install cssaw-central
```

## Usage

### csvsql script

The package comes with a script to automatically upload a csv file to the given table in a sql database. It takes user, pass, host IP, database, table, and cSV file path as arguments

#### example
``` Bash
csvsql test test HOST Test test_table ./TestDocs/test.csv
```

The above example connects to the Test database using the test user and inserts the test.csv file into test_table.

### Session module
Session object acts as a wrapper for sqlalchemy connection. The connection is created and stored in the Session object at initialization, and any results can be taken from the self.conn object or, if using execute_sql(), can be taken from the returned results python list.

#### Example:
```Python
from cssaw_central import Session

sess = Session('test','test', 'localhost', db='Test')

sess.create_table('test_table', ['column1', 'column2', 'column3'], \ 
                    ['int', 'int', 'int'], ['True', 'False', 'False'])

sess.insert('test_table', ['column1', 'column2', 'column3'], [0, 1, 2])
print(sess.execute_SQL('./queries/test.sql'))
```

The above script will create a connection to the Test database at localhost:3306 (assuming that it exists), insert the given values into their appropriate columns in test_table, and then execute test.sql from the queries file.

# To Do:
- Stripped implementation of SELECT
- Stripped implementation of UPDATE
- Stripped implementation of JOIN

# License
[MPL-2.0](https://opensource.org/licenses/MPL-2.0)