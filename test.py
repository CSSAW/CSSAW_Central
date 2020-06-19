from query import *
import datetime

def test_connect():
    host = open('host.txt')
    sess = Session('test', 'test', host.read())
    host.close()

    op = "SELECT * FROM test_table;"
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

if __name__ == '__main__':
    print('Test connect')
    test_connect()
    print('Connect successful')
    print('Execute SQL File Test')
    test_executeSQL()
    print('Successful SQL File Execution')
    print()
    print('Test Completed')