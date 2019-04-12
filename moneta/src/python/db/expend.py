# coding=utf-8

"""This module provides model for interaction with expend and user_expend tables"""
from datetime import datetime

from MySQLdb.cursors import DictCursor

from core.db.pool_manager import DBPoolManager


class Expend:
    """
    Model for manipulation data of Expend record in db.
    """

    @staticmethod
    def __execute_query(query, args):
        "this method execute transaction query via pool_manager"
        with DBPoolManager().get_cursor() as curs:
            curs.execute(query, args)

    @staticmethod
    def __get_from_db(query, args):
        "this method execute query and return some record from db as tuple of tuples"
        with DBPoolManager().get_connect() as conn:
            curs = conn.cursor(DictCursor)
            curs.execute(query, args)
            return curs.fetchall()

    @staticmethod
    def edit_name(expend_id, new_name):
        """this method """

        query = 'UPDATE expend SET name = %s WHERE id = %s;'
        args = (new_name, expend_id,)
        Expend.__execute_query(query, args)

    @staticmethod
    def edit_amount(expend_id, new_amount):
        """method for editing planned cost in expend"""
        query = 'UPDATE expend SET amount = %s WHERE id = %s;'
        args = (new_amount, expend_id,)
        Expend.__execute_query(query, args)

    @staticmethod
    def edit_image_id(expend_id, new_image_id):
        """method for editing image for expend"""
        query = 'UPDATE expend SET image_id = %s WHERE id = %s;'
        args = (new_image_id, expend_id,)
        Expend.__execute_query(query, args)

    @staticmethod
    def delete_expend_for_user(expend_id, user_id):
        "this method delete record from user_expend table"
        query = 'DELETE FROM user_expend WHERE expend_id = %s AND user_id = %s;'
        args = (expend_id, user_id,)
        Expend.__execute_query(query, args)

    @staticmethod
    def get_expend_by_id(expend_id):
        "this method return record of expend from db as tuple"
        query = 'SELECT * FROM expend WHERE id = %s;'
        args = (expend_id,)
        expend = Expend.__get_from_db(query, args)[0]
        print(expend)
        return expend

    @staticmethod
    def can_edit(expend_id, user_id):
        """
        Returns True if user can edit expend record, else returns False.
        :params: user_id - id of logged user, expend_id,
        :return: True or False
        """
        query = """
                SELECT can_edit
                FROM  user_expend
                WHERE user_id=%s AND expend_id=%s;
                """
        args = (user_id, expend_id)
        res = Expend.__get_from_db(query, args)[0]['can_edit']
        return bool(res)

    @staticmethod
    def __get_tuple_of_user_expends(user_id):
        "this method return tuple of expend_id which belong to user"
        query = 'select expend_id from user_expend where user_id = %s;'
        res = Expend.__get_from_db(query, (user_id,))
        user_expends = tuple(row['expend_id'] for row in res)
        return user_expends

    @staticmethod
    def get_user_expends_tuple_from_db(user_id):
        "this method return tuple of records of expends from db"
        user_expends = Expend.__get_tuple_of_user_expends(user_id)
        if len(user_expends) >= 2:
            query = f"SELECT * FROM expend WHERE id IN {user_expends};"
        elif len(user_expends) == 1:
            query = f"SELECT * FROM expend WHERE id = {user_expends[0]};"
        else:
            return tuple()

        return Expend.__get_from_db(query, ())

    @staticmethod
    def __get_last_expend():
        '''Getting last expend from database.'''
        query = """
            SELECT id from expend
            WHERE mod_time = (SELECT MAX(mod_time) FROM expend);"""
        return Expend.__get_from_db(query, ())

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
        currencies = Expend.__get_from_db(query, ())[0]['Type']
        def_currency = [item[1:-1] for item in currencies[5:-1].split(',')]
        return tuple(enumerate(def_currency))
