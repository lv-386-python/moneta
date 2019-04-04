"This module provides model for interaction with expend and user_expend tables"

from ..core.db.pool_manager import pool_manage


class Expend:
    """
    Model for manipulation data of Expend instance.
    """

    def __init__(self, expend_id, name, currency, image_id):
        '''Initiation fields of an Expend instance.'''
        self._id = expend_id
        self.name = name
        self.currency = currency
        self.image_id = image_id

    @staticmethod
    def execute_query(query):
        "this method execute transaction query via pool_manager"
        with pool_manage().transaction() as curs:
            curs.execute(query)

    @staticmethod
    def get_from_db(query):
        "this method execute query and return some record from db as tuple of tuples"
        with pool_manage().manage() as conn:
            curs = conn.cursor()
            curs.execute(query)
            return curs.fetchall()

    @staticmethod
    def edit_name(expend_id, new_name):
        """method for renaming expend"""

        query = f"""
            UPDATE expend
            SET name = "{new_name}"
            WHERE id = {expend_id};"""
        Expend.execute_query(query)

    @staticmethod
    def edit_planned_cost(expend_id, new_planned_cost):
        """method for editing planned cost in expend"""
        try:
            new_planned_cost = int(new_planned_cost)
        except ValueError:
            pass

        query = f"""
                UPDATE expend
                SET planned_cost = {new_planned_cost}
                WHERE id = {expend_id}"""
        Expend.execute_query(query)

    @staticmethod
    def edit_image_id(expend_id, new_image_id):
        """method for editing image for expend"""
        query = f"""
                UPDATE expend
                SET image_id = {new_image_id}
                WHERE id = {expend_id};"""
        Expend.execute_query(query)

    @staticmethod
    def delete_expend_for_user(expend_id, user_id):
        "this method delete record from user_expend table"
        query = f"""
                    DELETE FROM user_expend
                    WHERE user_id = {user_id} AND expend_id = {expend_id};"""
        Expend.execute_query(query)

    @staticmethod
    def get_expend_by_id(expend_id):
        "this method return record of expend from db as tuple"
        query = f"SELECT * FROM expend WHERE id = {expend_id}"
        expend = Expend.get_from_db(query)[0]
        return expend

    @staticmethod
    def get_tuple_of_user_expends(user_id):
        "this method return tuple of expend_id which belong to user"
        query = f"select expend_id from user_expend where user_id ={user_id};"
        res = Expend.get_from_db(query)
        user_expends = tuple(expend_id[0] for expend_id in res)
        return user_expends

    @staticmethod
    def get_user_expends_tuple_from_db(user_id):
        "this method return tuple of records of expends from db"
        user_expends = Expend.get_tuple_of_user_expends(user_id)
        if len(user_expends) >= 2:
            query = f"SELECT * FROM expend WHERE id IN {user_expends};"
        elif len(user_expends) == 1:
            query = f"SELECT * FROM expend WHERE id = {user_expends[0]};"
        else:
            return tuple()
        return Expend.get_from_db(query)
