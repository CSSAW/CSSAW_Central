import sqlalchemy as alc
import logging
import pandas as pd

class Session:
    def __init__(self, user, password, host, db='Test'):
        """ Initialize connection to database

            args:
                user ---- name of user to connect as
                password ---- password for specified user
                host ---- host ip to connect to

            kwargs:
                db ---- database to connect to (defaults to test)
        """
        self.engine = alc.create_engine("mysql+pymysql://{}:{}@{}/{}".format(user, password, host, db), echo=True)

        self.meta = MetaData(self.engine)

        self.conn = self.engine.connect()

    def execute_SQL(self, filename):
        """ execute .SQL file of commands 
        
            args:
                filename ---- path of file to execute (must be .sql)
        """

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
        """ insert given rows into given table.
            Creates table if it doesn't already exist.
        
            args:
                table ---- name of table to insert into
                columns ---- list of column names
                rows ---- list of lists of values to put into corresponding columns

                len(columns) MUST EQUAL len(rows)
        """

        df = pd.DataFrame(data=rows, columns=columns)

        if not alc.engine.Dialect.has_table(self.conn, table):
            self.create_table(df)
        
        try:
            df.to_sql(table, self.conn, if_exists='append', index=False)
        except ValueError as e:
            print(e)
            quit()

    def insert_from_CSV(self, filename, table):
        """ Inserts entire CSV file into specified table.
            Creates table if it doesn't already exist.

            args:
                filename ---- file path of data to upload
                table ---- name of table to insert into

        """
        df = pd.read_csv(filename)
        try:
            df.to_sql(table, self.engine, if_exists='append', index=False)
        except ValueError as e:
            print(e)
            quit() 

    def create_table(self, dataframe):
        """ create table from given dataframe

            args:
                dataframe ---- dataframe to base table off of
        """

        # create table with dataframe data
        sql_table = alc.Table(
            table, self.meta,
            *(alc.Column(
                column_name, column_type)
                for column_name, column_type
                in zip(columns, list(dataframe.dtypes))))

        # create table in database
        self.meta.create_all(self.engine)