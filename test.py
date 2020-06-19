from query import *
import datetime

def test_connect():
    crsr = connect('test', 'test', open('host.txt').read())
    assert crsr != None
    assert len(crsr.column_names == 2) & crsr.column_names[0] == u'column1' & crsr.column_names[1] == u'column2'

def test_executeSQL():
    crsr = connect('test', 'test', open('host.txt').read())

    execute_SQL('./queries/test.sql', crsr)

    buffer = []
    for row in crsr:
        buffer.append(row)

    assert buffer[0]['column1'] + buffer[0]['column2'] == '6/18/2020test'

if __name__ == '__main__':
    test_connect()
    test_executeSQL()