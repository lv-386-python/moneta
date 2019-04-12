"""
Module for interaction with a current table in a database.
"""
from MySQLdb._exceptions import IntegrityError

from core.db.db_helper import DbHelper


class Current(DbHelper):
    """
    Model for interacting with a current table in a database.
    """

    # TODO Vasyl # pylint: disable=fixme
    @staticmethod
    def create_current():
        """

        :return:
        """
        sql = f"""
            INSERT IGNORE INTO user_current(user_id, current_id, can_edit, is_owner)
            VALUES (%s, %s, %s, %s);
            """
        args = (1, 10, 1, 1)
        Current._make_transaction(sql, args)

    @staticmethod
    def edit_current(user_id, current_id, name, mod_time, image_id):  # pylint: disable=unused-argument
        """
        Edits a current table in a database.
        :params: user_id - id of logged user, current_id - id of edited current,
                 name - new name for current, mod_time - modification time,
                 image_id - image for current
        :return: True if success, else False
        """
        sql = f"""
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
        sql = f"""
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
        sql = f"""
            SELECT
                c.id, c.name, c.currency,
                c.mod_time, c.amount,
                i.css, user_current.can_edit, user_current.is_owner
            FROM user_current
            LEFT JOIN current c ON user_current.current_id = c.id
            LEFT JOIN image i ON c.image_id = i.id
            WHERE user_current.user_id=%s
            ORDER BY c.name;
            """
        args = (user_id, )
        query = Current._make_select(sql, args)
        return query

    @staticmethod
    def get_current_by_id(user_id, current_id):
        """
        Gets a current by id for a logged user.
        :params: user_id - id of logged user, current_id - id of current
        :return: current instance
        """
        sql = f"""
            SELECT
                c.id, c.name, c.currency,
                c.mod_time, c.amount,
                i.css, user_current.can_edit, user_current.is_owner
            FROM user_current
            LEFT JOIN current c ON user_current.current_id = c.id
            LEFT JOIN image i ON c.image_id = i.id
            WHERE user_current.user_id=%s AND c.id=%s
            ORDER BY c.name;
            """
        args = (user_id, current_id)
        query = Current._make_select(sql, args)
        if not query:
            return None
        return query[0]

    @staticmethod
    def can_edit_current(user_id, current_id):
        """
        Returns True if user can edit a current, else returns False.
        :params: user_id - id of logged user, current_id - id of current
        :return: True or False
        """
        sql = f"""
            SELECT can_edit
            FROM  user_current
            WHERE user_id=%s AND current_id=%s;
            """
        args = (user_id, current_id)
        query = Current._make_select(sql, args)
        try:
            # check value of can_edit field
            if query[0]['can_edit'] == 1:
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
                         where current_id=%s
                         and is_owner=0) 
            order by email;
            """
        args = (current_id,)
        query = Current._make_select(sql, args)
        if not query:
            return None
        return(query)

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
        query = Current._make_transaction(sql, args)

    @staticmethod
    def share(current_id, user_id, can_edit):
        """
        Gets a current by id for a logged user.
        :params: user_id - id of logged user, current_id - id of current
        :return: current instance
        """
        sql = f"""
            select id from auth_user where email=%s;
            """

        id_user = Current._make_select(sql, (user_id,))[0]['id']
        print(id_user)

        sql = f"""
            INSERT INTO user_current(user_id, current_id, can_edit, is_owner)
            VALUES (%s, %s, %s, %s);
            """
        args = (id_user, current_id, can_edit, '0')
        query = Current._make_transaction(sql, args)
