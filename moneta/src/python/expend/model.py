from datetime import datetime
import MySQLdb

DB_NAME = 'db_moneta'
DB_USER = 'moneta_user'
DB_PASS = 'hroM0507@Kot'


class Expend:
    '''
    Model for manipulation data regarding Expend instance.
    '''

    def __init__(self, name, currency, image_id):
        '''Initiation fields of an Expend istance.'''
        self.name = name
        self.currency = currency
        self.image_id = image_id
        self.create_time = datetime.now().timestamp()
        self.modification_time = self.create_time

    def create(self):
        CONNECTION = MySQLdb.connect(user=DB_USER, passwd=DB_PASS, db=DB_NAME)
        cursor = CONNECTION.cursor()
        # getting required id from db
        with cursor:
            cursor.execute("select max(id) from expend;")
            expend_id = cursor.fetchall()[0][0] + 1

        # insertation query
        query = f"""
            INSERT INTO expend (id, name, currency, create_time, modification_time, image_id)
            VALUES ('{expend_id}', '{self.name}', '{self.currency}',
        {self.create_time}, {self.modification_time}, '{self.image_id}')
        ;"""
        Expend.execute_query(query)

    @staticmethod
    def execute_query(query):
        '''Connecting to database and executing query'''
        CONNECTION = MySQLdb.connect(user=DB_USER, passwd=DB_PASS, db=DB_NAME)
        cursor = CONNECTION.cursor()
        try:
            # Execute the SQL command
            cursor.execute(query)
            # Commit your changes in the database
            CONNECTION.commit()
        except Exception:
            # Rollback in case there is any error
            CONNECTION.rollback()
        CONNECTION.close()

    @staticmethod
    def edit_name(expend_id, new_name):
        '''method for renaming expend'''

        query = f"""
            UPDATE expend
            SET name = '{new_name}'
            WHERE id = {expend_id};"""
        Expend.execute_query(query)

    @staticmethod
    def edit_planned_cost(expend_id, new_planned_cost):
        '''method for editting planned cost in expend'''

        query = f"""
                UPDATE expend
                SET planned_cost = {new_planned_cost}
                WHERE id = {expend_id};"""
        Expend.execute_query(query)

    @staticmethod
    def edit_image_id(expend_id, new_image_id):
        '''method for editting image for expend'''

        query = f"""
                UPDATE expend
                SET image_id = {new_image_id}
                WHERE id = {expend_id};"""
        Expend.execute_query(query)
