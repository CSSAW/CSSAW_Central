"""
Author: Luke Williams

CSSAW Python SQL helpers

(Will eventually become a command line program for executing sql scripts
in the python shell)

"""

import os
import mysql.connector
from mysql import OperationalError
import argparse
import logging

def executeSQL(filename, cursor):
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