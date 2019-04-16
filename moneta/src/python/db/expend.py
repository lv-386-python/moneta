'''Module for manipulation data regarding Expend instance..'''
from datetime import datetime
from MySQLdb.cursors import DictCursor

from core.db.pool_manager import DBPoolManager


class Expend:
    '''
    Model for manipulation data regarding Expend instance.
    '''
    @staticmethod
    def __execute_query(query, args):
        '''Connecting to database and executing query.'''
        with DBPoolManager().get_cursor() as curs:
            # Execute the SQL command
            curs.execute(query, args)

    @staticmethod
    def __get_from_db(query):
        '''Connecting to database and reterning result of SELECT.'''
        with DBPoolManager().get_connect() as conn:
            cursor = conn.cursor(DictCursor)
            cursor.execute(query)
            result = cursor.fetchall()
        return result

    @staticmethod
    def __get_last_expend():
        '''Getting last expend from database.'''
        query = """
            SELECT id from expend
            WHERE mod_time = (SELECT MAX(mod_time) FROM expend);"""
        return Expend.__get_from_db(query)

    @staticmethod
    def create_expend(name, currency, amount, image_id):
        '''Creating new expend'''
        create_time = datetime.now().timestamp()
        mod_time = create_time
        query = """
            INSERT INTO expend (name, currency, create_time, mod_time, amount, image_id)
            VALUES (%s, %s, %s, %s, %s, %s);"""
        args = (name, currency, create_time, mod_time, amount, image_id)
        Expend.__execute_query(query, args)

    @staticmethod
    def create_user_expend(user_id):
        '''Creating new record in user_expend table.'''
        query = """
            INSERT INTO user_expend (user_id, expend_id, can_edit)
            VALUES (%s, %s, %s)"""
        expend_id = Expend.__get_last_expend()[0]['id']
        can_edit = 1
        args = (user_id, expend_id, can_edit)
        Expend.__execute_query(query, args)

    @staticmethod
    def get_default_currencies():
        '''Getting all available currencies from database.'''
        query = """SHOW COLUMNS FROM user where Field='def_currency';"""
        currencies = Expend.__get_from_db(query)[0]['Type']
        def_currency = [item[1:-1] for item in currencies[5:-1].split(',')]
        return tuple(enumerate(def_currency))
