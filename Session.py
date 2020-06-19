import mysql.connector
from mysql.connector.errors import OperationalError
import logging

class Session:
    def __init__(self, user, password, host, db='Test'):
        self.user = user
        self.password = password
        self.host = host
        self.db = db

        self.conn = mysql.connector.connect(
            user=self.user,
            password=self.password,
            host=self.host,
            database=self.db
        )

        self.cursor = self.conn.cursor(dictionary=True, buffered=True)

    def __del__(self):
        self.cursor.close()
        self.conn.close()

    def execute_SQL(self, filename):
        """ execute .SQL file of commands """

        # open file

        file = open(filename, 'r', encoding='utf-8-sig')
        sql = file.read()
        file.close()

        # get commands
        commands = sql.split(';')
        commands.pop()

        # execute commands
        for command in commands:
            command = command.strip()
            try:
                self.cursor.execute(command)
            except mysql.connector.OperationalError:
                logging.error('Operation \"' + command + '\" failed, skipping...')