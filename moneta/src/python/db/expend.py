# coding=utf-8

"""This module provides model for interaction with expend and user_expend tables"""
from datetime import datetime

from core.db.db_helper import DbHelper


class Expend(DbHelper):
    """
    Model for manipulation data of Expend record in db.
    """

    @staticmethod
    def edit_name(expend_id, new_name):
        """
        Method for update expend name,
        take expend_id as int and new_name as str
        """

        query = 'UPDATE expend SET name = %s WHERE id = %s;'
        args = (new_name, expend_id,)
        Expend._make_transaction(query, args)

    @staticmethod
    def edit_amount(expend_id, new_amount):
        """
        Method for editing planned cost in expend
        take expend_id as int and new_amount as int
        """
        query = 'UPDATE expend SET amount = %s WHERE id = %s;'
        args = (new_amount, expend_id,)
        Expend._make_transaction(query, args)

    @staticmethod
    def edit_image_id(expend_id, new_image_id):
        """
        Method for editing image for expend
        take expend_id as int and new_image_id as int
        """
        query = 'UPDATE expend SET image_id = %s WHERE id = %s;'
        args = (new_image_id, expend_id,)
        Expend._make_transaction(query, args)

    @staticmethod
    def delete_expend_for_user(expend_id, user_id):
        """
        This method delete record from user_expend table
        take expend_id as int and user_id as int
        """
        query = 'DELETE FROM user_expend WHERE expend_id = %s AND user_id = %s;'
        args = (expend_id, user_id,)
        Expend._make_transaction(query, args)

    @staticmethod
    def get_expend_by_id(expend_id):
        """
        This method return record of expend from db as tuple
        take expend_id as int
        return expend as dict
        """
        query = 'SELECT * FROM expend WHERE id = %s;'
        args = (expend_id,)
        response = Expend._make_select(query, args)
        if response:
            expend = response[0]
        else:
            expend = ()
        return expend

    @staticmethod
    def can_edit(expend_id, user_id):
        """
        Check if user can edit expend.
        takes user_id - id of logged user as int, expend_id as int
        return: True or False
        """
        query = """
                SELECT can_edit
                FROM  user_expend
                WHERE user_id=%s AND expend_id=%s;
                """
        args = (user_id, expend_id)
        res = Expend._make_select(query, args)[0]['can_edit']
        return bool(res)

    @staticmethod
    def __get_tuple_of_user_expends(user_id):
        """
        This method return tuple of expend_id which belong to user
        takes user_id as int
        return tuple of id of user expends
        """
        query = 'select expend_id from user_expend where user_id = %s;'
        res = Expend._make_select(query, (user_id,))
        user_expends = tuple(row['expend_id'] for row in res)
        return user_expends

    @staticmethod
    def get_user_expends_tuple_from_db(user_id):
        """
        This method return tuple of records of expends from db
        takes user_id as int
        return tuple of user's expands or empty tuple if user doesn't have any
        """
        user_expends = Expend.__get_tuple_of_user_expends(user_id)
        if len(user_expends) >= 2:
            query = f"SELECT * FROM expend WHERE id IN {user_expends};"
        elif len(user_expends) == 1:
            query = f"SELECT * FROM expend WHERE id = {user_expends[0]};"
        else:
            return tuple()

        return Expend._make_select(query, ())

    @staticmethod
    def __get_last_expend():
        '''Getting last expend from database.'''
        query = """
            SELECT id from expend
            WHERE mod_time = (SELECT MAX(mod_time) FROM expend);"""
        return Expend._make_select(query, ())

    @staticmethod
    def create_expend(name, currency, amount, image_id):
        '''Creating new expend'''
        create_time = datetime.now().timestamp()
        mod_time = create_time
        query = """
            INSERT INTO expend (name, currency, create_time, mod_time, amount, image_id)
            VALUES (%s, %s, %s, %s, %s, %s);"""
        args = (name, currency, create_time, mod_time, amount, image_id)
        Expend._make_transaction(query, args)

    @staticmethod
    def create_user_expend(user_id):
        '''Creating new record in user_expend table.'''
        query = """
            INSERT INTO user_expend (user_id, expend_id, can_edit)
            VALUES (%s, %s, %s)"""
        expend_id = Expend.__get_last_expend()[0]['id']
        can_edit = 1
        args = (user_id, expend_id, can_edit)
        Expend._make_select(query, args)

    @staticmethod
    def get_default_currencies():
        '''Getting all available currencies from database.'''
        query = """SHOW COLUMNS FROM user where Field='def_currency';"""
        currencies = Expend._make_select(query, ())[0]['Type']
        def_currency = [item[1:-1] for item in currencies[5:-1].split(',')]
        return tuple(enumerate(def_currency))
