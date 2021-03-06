"""
Module for interaction with a current table in a database.
"""
from datetime import datetime

from MySQLdb._exceptions import IntegrityError
from core.db.db_helper import DbHelper


class Current(DbHelper):
    """
    Model for interacting with a current table in a database.
    """

    @staticmethod
    def create_current(name, currency, amount, image_id, owner_id, user_id):
        """Creating new current"""
        query = """
                INSERT INTO current (name, currency, create_time, mod_time, amount, image_id, owner_id)
                VALUES (%s, %s, %s, %s, %s, %s, %s);
                INSERT INTO user_current (user_id, current_id, can_edit)
                VALUES (%s, LAST_INSERT_ID(), %s);"""
        cr_time = datetime.now().timestamp()
        mod_time = cr_time
        can_edit = 1
        args = (name, currency, cr_time, mod_time, amount, image_id, owner_id, user_id, can_edit)
        try:
            Current._make_transaction(query, args)
        except IntegrityError:
            return False
        return True

    @staticmethod
    def check_if_such_current_exist(owner_id, name, currency):
        """Method for checking
         if current with such name
        and same currency already
        exist in db, and user is his owner"""
        query = """
                SELECT * FROM current WHERE owner_id = %s AND name = %s AND currency = %s;"""
        args = (owner_id, name, currency)
        query_result = Current._make_select(query, args)
        return query_result

    @staticmethod
    def edit_current(user_id, current_id, name, mod_time, image_id):  # pylint: disable=unused-argument
        """
        Edits a current table in a database.
        :params: user_id - id of logged user, current_id - id of edited current,
                 name - new name for current, mod_time - modification time,
                 image_id - image for current
        :return: True if success, else False
        """
        sql = """
            UPDATE current
            SET name=%s, mod_time=%s, image_id=%s
            WHERE current.id=%s;
            """
        args = (name, mod_time, image_id, current_id)
        try:
            Current._make_transaction(sql, args)
        except IntegrityError:
            return False
        return True

    @staticmethod
    def delete_current(user_id, current_id):
        """
        Deletes connection between a user and a current in a database.
        :params: user_id - id of logged user, current_id - id of  current,
        :return: True if success, else False
        """
        sql = """
            DELETE FROM user_current
            WHERE current_id=%s AND user_id=%s;
            """
        args = (current_id, user_id)
        try:
            Current._make_transaction(sql, args)
        except IntegrityError:
            return False
        return True

    @staticmethod
    def get_current_list_by_user_id(user_id):
        """
        Gets a list of currents for a logged user.
        :params: user_id - id of logged user
        :return: list of currents
        """
        sql = """
            SELECT
                c.id, c.name, cs.currency, c.currency as currency_id,
                c.mod_time, c.amount,
                i.css, user_current.can_edit
            FROM user_current
            LEFT JOIN current c ON user_current.current_id = c.id
            LEFT JOIN image i ON c.image_id = i.id
            LEFT JOIN currencies cs ON c.currency = cs.id
            WHERE user_current.user_id=%s
            ORDER BY c.name;
            """
        args = (user_id,)
        query_result = Current._make_select(sql, args)
        return query_result

    @staticmethod
    def get_current_by_id(user_id, current_id):
        """
        Gets a current by id for a logged user.
        :params: user_id - id of logged user, current_id - id of current
        :return: current instance
        """
        sql = """
            SELECT
                c.id, c.name, c.owner_id, cs.currency, c.currency as currency_id,
                c.mod_time, c.amount, i.id as image_id,
                i.css, user_current.can_edit
            FROM user_current
            LEFT JOIN current c ON user_current.current_id = c.id
            LEFT JOIN image i ON c.image_id = i.id
            LEFT JOIN currencies cs ON c.currency = cs.id
            WHERE user_current.user_id=%s AND c.id=%s
            ORDER BY c.name;
            """
        args = (user_id, current_id)
        query_result = Current._make_select(sql, args)
        if not query_result:
            return None
        return query_result[0]

    @staticmethod
    def can_edit_current(user_id, current_id):
        """
        Returns True if user can edit a current, else returns False.
        :params: user_id - id of logged user, current_id - id of current
        :return: True or False
        """
        sql = """
            SELECT can_edit
            FROM  user_current
            WHERE user_id=%s AND current_id=%s;
            """
        args = (user_id, current_id)
        query_result = Current._make_select(sql, args)
        try:
            # check value of can_edit field
            if query_result[0]['can_edit'] == 1:
                return True
            return False
        except IndexError:
            return False

    @staticmethod
    def get_users_list_by_current_id(current_id):
        """
        Gets a current by id for a logged user.
        :params: user_id - id of logged user, current_id - id of current
        :return: current instance
        """
        sql = f"""
            select id as user_id, email 
            from auth_user 
            where id in (select user_id 
                         from user_current 
                         where current_id=%s)
            and id not in (select owner_id from current where id=%s);
            """
        args = (current_id, current_id)
        query = Current._make_select(sql, args)
        if not query:
            return []
        return query

    @staticmethod
    def cancel_sharing(current_id, user_id):
        """
        Gets a current by id for a logged user.
        :params: user_id - id of logged user, current_id - id of current
        :return: current instance
        """
        sql = f"""
            delete from user_current
            where current_id=%s and user_id=%s;
            """
        args = (current_id, user_id)
        Current._make_transaction(sql, args)

    @staticmethod
    def share(current_id, user_id, can_edit):
        """
        Gets a current by id for a logged user.
        :params: user_id - id of logged user, current_id - id of current
        :return: current instance
        """
        sql = f"""
            INSERT INTO user_current(user_id, current_id, can_edit)
            VALUES (%s, %s, %s);
            """
        args = (user_id, current_id, can_edit)
        Current._make_transaction(sql, args)
