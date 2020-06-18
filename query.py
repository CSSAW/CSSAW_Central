"""
Author: Luke Williams

CSSAW Python SQL helpers

(Will eventually become a command line program for executing sql scripts
in the python shell)

"""

import mysql.connector
from mysql import OperationalError
import argparse
import logging
import json

def connect(user, password, host):
    """ connects to database and returns dict cursor """

    try:
        cnct = mysql.connector.connect(
            user=user,
            password=password,
            host=host,
            database='CENTRAL'
        )
        return cnct.cursor(dictionary=True)
    except mysql.connector.Error as err:
        logging.error("Connection error: ", err)

def execute_SQL(filename, cursor):
    """ execute .SQL file of commands """

    # open file
    file = open(filename, 'r')
    sql = file.read()
    file.close()

    # get commands
    commands = sql.split(';')

    # execute commands
    for command in commands:
        try:
            cursor.execute(command)
        except mysql.connector.OperationalError:
            logging.error('Operation \"' + command '\" failed, skipping...')

def get_JSON_from_cursor(cursor):
    """ Return JSON string from cursor results """

    outS = ''
    for result in cursor:
        outS += json.dumps(result, JSONout, indent=4)

    return outS

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('host', help='Host IP for server')
    parser.add_argument('user', help='Database account for login')
    parser.add_argument('password', default=None, help='Password for database user')
    parser.add_argument('querypath', help='Path of query to execute')
    parser.add_argument('-outfile', default='./results/result.json', help='Filename of output json file')
    args = parser.parse_args()

    # connect to server using given user and pass
    cursor = connect(args.user, args.password, args.host)

    # execute external sql file
    execute_SQL(args.querypath, cursor)

    with open(args.outfile, 'w+') as outfile:
        outfile.write(get_JSON_from_cursor(cursor))