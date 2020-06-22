import mysql.connector
import sqlalchemy as alc
from mysql.connector.errors import OperationalError
import logging

class Session:
    def __init__(self, user, password, host, db='Test'):
        self.engine = alc.create_engine("mysql+pymysql://{}:{}@{}/{}".format(user, password, host, db))

        self.conn = self.engine.connect()

    def execute_SQL(self, filename):
        """ execute .SQL file of commands """

        # open file

        file = open(filename, 'r', encoding='utf-8-sig')
        sql = file.read()
        file.close()

        # get commands
        commands = sql.split(';')
        commands.pop()
        
        results = []

        # execute commands
        for command in commands:
            command = command.strip()
            try:
                results.append(self.conn.execute(alc.sql.text(command)))
            except:
                logging.error('Operation \"' + command + '\" failed, skipping...')

        return results

    def insert(self, table, columns, rows):
        """ insert given rows into given table """

        # query type
        query = alc.insert(table)

        # build list of rows to insert
        values_list = []
        for row in rows:
            values_list.append(dict(zip(columns, row)))

        # execute and commit query
        self.conn.execute(query, values_list)

    def insert_from_CSV(self, filename, table, primary_key):
        with open(filename, 'r') as f:

            # pull headers
            headers = f.readline().split(',')

            # get csv rows
            lines = f.readlines()

            # convert rows into list of lists
            rows = [[x.strip()] for x in line.split(',') for line in lines]

            # user insert member function to insert
            try:
                self.insert(table, headers, rows)
            except:
                logging.error('Insert failed for file: %s' % filename)

    def create_table(self, table_name, columns, types, primary_key_flags):
        """ Creates table from given parameters 
        
            args:
                table_name ---- name of table
                columns ---- list of columns
                types ---- list of column types
                primary_key_flags ---- list of bools denoting whether column is primary key

        """
        
        meta = alc.MetaData()

        table = alc.Table(
            table_name, meta,
            *(alc.Column(column_name, column_type,
                    primary_key=columns)
            for column_name,
            column_type,
            primary_key_flag in zip(
                                columns,
                                types,
                                primary_key_flags)))
            
        table.create()