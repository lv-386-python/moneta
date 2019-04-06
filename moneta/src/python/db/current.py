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
            START TRANSACTION;
            INSERT IGNORE INTO user_current(user_id, current_id, can_edit)
            VALUES (1, 10, 1);
            COMMIT;
            """
        Current._make_transaction(sql)

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
            SET name='{name}', mod_time={mod_time}, image_id={image_id}
            WHERE current.id={current_id}; 
            """
        try:
            Current._make_transaction(sql)
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
            WHERE current_id={current_id} AND user_id={user_id};
            """
        try:
            Current._make_transaction(sql)
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
                i.css, user_current.can_edit
            FROM user_current
            LEFT JOIN current c ON user_current.current_id = c.id
            LEFT JOIN image i ON c.image_id = i.id
            WHERE user_current.user_id={user_id}
            ORDER BY c.name;
            """
        query = Current._make_select(sql)
        current_list = []
        for row in query:
            current_list.append({
                'current_id': row['id'],
                'name': row['name'],
                'currency': row['currency'],
                'mod_time': row['mod_time'],
                'amount': row['amount'],
                'image_css': row['css'],
                'can_edit': row['can_edit']
            })
        return current_list

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
                i.css, user_current.can_edit
            FROM user_current
            LEFT JOIN current c ON user_current.current_id = c.id
            LEFT JOIN image i ON c.image_id = i.id
            WHERE user_current.user_id={user_id} AND c.id={current_id}
            ORDER BY c.name;
            """

        query = Current._make_select(sql)
        if not query:
            return None
        query = query[0]
        current = {
            'current_id': query['id'],
            'name': query['name'],
            'currency': query['currency'],
            'mod_time': query['mod_time'],
            'amount': query['amount'],
            'image_css': query['css'],
            'can_edit': query['can_edit']
        }

        return current

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
            WHERE user_id={user_id} AND current_id={current_id};
            """
        query = Current._make_select(sql)
        try:
            # check value of can_edit field
            if query[0]['can_edit'] == 1:
                return True
            return False
        except IndexError:
            return False
