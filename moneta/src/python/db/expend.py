# coding=utf-8

"""
    This module provides model for interaction with expend and user_expend tables

"""
from datetime import datetime

from core.db.db_helper import DbHelper
from core.utils import get_logger

# Get an instance of a LOGGER
LOGGER = get_logger(__name__)


class Expend(DbHelper):
    """
    Model for manipulation data of Expend record in db.

    """

    @staticmethod
    def update(expend_id, new_name=None, new_amount=None, new_image_id=None):
        """
        Method for update expend record in table

        Args:
            expend_id (int) : id of expend record,
            new_name (str) : new name for record. Defaults to None.
            new_amount (float) : new amount for expend. Defaults to None.
            new_image_id (int) : id of new image for expend. Defaults to None.

        """
        args = []
        query_args = []
        if new_name:
            query_args.append('name = %s')
            args.append(new_name)
        if new_amount:
            query_args.append('amount = %s')
            args.append(new_amount)
        if new_image_id:
            query_args.append('image_id = %s')
            args.append(new_image_id)

        query = 'UPDATE expend SET %s WHERE id = %s;' % (','.join(query_args), expend_id)
        Expend._make_transaction(query, args)
        LOGGER.info('expend %s was updated with query %s, %s.', expend_id, query, args)

    @staticmethod
    def delete_expend_for_user(expend_id, user_id):
        """
        This method delete record from user_expend table

        Args:
            expend_id (int) : id of expend record,
            user_id (int) : id of user

        """
        query = 'DELETE FROM user_expend WHERE expend_id = %s AND user_id = %s;'
        args = (expend_id, user_id,)
        Expend._make_transaction(query, args)
        LOGGER.info('expend %s deleted for user %s.', expend_id, user_id)

    @staticmethod
    def get_expend_by_id(expend_id):
        """
        This method return record of expend from db as tuple
        Args:
            expend_id (int) : id of expend record,

        Returns:
             expend record as dict if successful, otherwise empty tuple.
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
        Check if user has permission to edit expend record.

        Args:
            user_id(int): id of logged user.
            expend_id(int) : id of expend.
        Returns:
             True or False.
        """

        query = 'SELECT can_edit FROM  user_expend WHERE user_id=%s AND expend_id=%s;'

        args = (user_id, expend_id)
        res = Expend._make_select(query, args)[0]['can_edit']
        return bool(res)

    @staticmethod
    def get_user_expends_tuple_from_db(user_id):
        """
        This method return tuple of records of expends from db.
        Args:
            user_id (int) : id of logged user.
        Returns:
            tuple of user's expands or empty tuple if user doesn't have any
        """
        query_ids = 'SELECT expend_id FROM user_expend WHERE user_id = %s;'
        response = Expend._make_select(query_ids, (user_id,))
        user_expends = tuple(row['expend_id'] for row in response)

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
        query = """SHOW COLUMNS FROM user_settings where Field='def_currency';"""
        currencies = Expend._make_select(query, ())[0]['Type']
        def_currency = [item[1:-1] for item in currencies[5:-1].split(',')]
        return tuple(enumerate(def_currency))

    @staticmethod
    def get_users_list_by_expend_id(expend_id):
        """
        Gets a expend by id for a logged user.
        :params: user_id - id of logged user, expend_id - id of expend
        :return: expend instance
        """
        sql = f"""
            select id as user_id, email 
            from auth_user 
            where id in (select user_id 
                         from user_expend 
                         where expend_id=%s
                         and is_owner=0) 
            order by email;
            """
        args = (expend_id,)
        query = Expend.__get_from_db(sql, args)
        if not query:
            return []
        return(query)

    @staticmethod
    def cancel_sharing(expend_id, user_id):
        """
        Gets a expend by id for a logged user.
        :params: user_id - id of logged user, expend_id - id of expend
        :return: expend instance
        """
        sql = f"""
            delete from user_expend
            where expend_id=%s and user_id=%s;
            """
        args = (expend_id, user_id)
        query = Expend.__execute_query(sql, args)

    @staticmethod
    def share(expend_id, post):
        """
        Gets a expend by id for a logged user.
        :params: user_id - id of logged user, expend_id - id of expend
        :return: expend instance
        """
        users = list(x['email'] for x in Expend.get_users_list_by_expend_id(expend_id))
        user_email = post['email']
        if user_email not in users:
            can_edit = 0
            if  'can_edit' in post:
                can_edit = 1
            sql = f"""
                select id from auth_user where email=%s;
                """

            id_user = Expend.__get_from_db(sql, (user_email,))[0]['id']
            sql = f"""
                INSERT INTO user_expend(user_id, expend_id, can_edit, is_owner)
                VALUES (%s, %s, %s, %s);
                """
            args = (id_user, expend_id, can_edit, '0')
            query = Expend.__execute_query(sql, args)
