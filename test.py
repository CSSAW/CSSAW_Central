from query import *
import datetime

def test_connect():
    host = open('host.txt')
    sess = Session('test', 'test', host.read())
    host.close()

    op = "SELECT * FROM test_table WHERE column1 = \'6/18/2020\';"
    sess.cursor.execute(op)
    for row in sess.cursor:
        print(row['column1'], row['column2'])
        assert (row['column1'] == '6/18/2020') & (row['column2'] == 'test')

def test_executeSQL():
    host = open('host.txt')
    sess = Session('test', 'test', host.read())
    host.close()

    try:
        sess.execute_SQL('./queries/test.sql')
    except mysql.connector.errors.Error as err:
        logging.error('Error: {}'.format(err))

def test_insert():
    host = open('host.txt')
    sess = Session('test', 'test', host.read())
    host.close()

    try:
        sess.insert('test_table', ['column1', 'column2'], [['6/19/2020', 'test']])
    except mysql.connector.errors.Error as err:
        print(err)

    result = sess.cursor.execute("""SELECT * FROM test_table WHERE column1 = \'6/19/2020\';""", multi=True)
    if result == None:
        logging.error('Insert failed')
        return

    for row in result:
        assert row.with_rows == True

if __name__ == '__main__':
    print('Test connect')
    test_connect()
    print('Connect successful')
    print('Execute SQL File Test')
    test_executeSQL()
    print('Successful SQL File Execution')
    print('Testing insert')
    test_insert()
    print('Insert finished')
    print()
    print('Test Completed')