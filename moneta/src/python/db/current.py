"""
Module for interaction with a current table in a database.
"""
try:
    from MySQLdb._exceptions import IntegrityError
except ImportError:
    pass

from src.python.core.db import db_helper as db


class Current:
    """
    Model for interacting with a current table in a database.
    """
    # def __init__(self, current_id, name, currency, create_time, mod_time,
    #              amount, image_css, can_edit):
    #     self.current_id = current_id
    #     self.name = name
    #     self.currency = currency
    #     self.create_time = create_time
    #     self.mod_time = mod_time
    #     self.amount = amount
    #     self.image_css = image_css
    #     self.can_edit = can_edit
    #
    # def __repr__(self):
    #     return f"<{self.current_id} {self.name}>"
    #
    # def __str__(self):
    #     return f"id:{self.current_id} name:{self.name}"

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
        db.insert_update_delete_sql(sql)
        # self._insert_update_delete_sql(sql)

    @staticmethod
    def edit_current(user_id, current_id, name, mod_time, image_id): # pylint: disable=unused-argument
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
            db.insert_update_delete_sql(sql)
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
            db.insert_update_delete_sql(sql)
        except IntegrityError:
            return False
        return True

    @staticmethod
    def get_current_list_by_user_id(user_id):
        """
        Gets a list of currents for a logged user.
        :params: user_id - id of logged user
        :return: tuple of currents
        """
        sql = f"""
            SELECT
                c.id, c.name, c.currency,
                c.create_time, c.mod_time, c.amount,
                i.css, user_current.can_edit
            FROM user_current
            LEFT JOIN current c ON user_current.current_id = c.id
            LEFT JOIN image i ON c.image_id = i.id
            WHERE user_current.user_id={user_id}
            ORDER BY c.name;
            """
        query = db.select_sql(sql)
        current_list = []
        for row in query:
            current_list.append(
                {
                    'current_id': row[0],
                    'current_name': row[1],
                    'current_mod_time': row[2],
                }
            )
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
                c.create_time, c.mod_time, c.amount,
                i.css, user_current.can_edit
            FROM user_current
            LEFT JOIN current c ON user_current.current_id = c.id
            LEFT JOIN image i ON c.image_id = i.id
            WHERE user_current.user_id={user_id} AND c.id={current_id}
            ORDER BY c.name;
            """

        query = db.select_sql(sql)
        print("get_current_by_id", query)
        if not query:
            return None
        query = query[0]
        current = Current(*query)
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
        query = db.select_sql(sql)
        try:
            # check value of can_edit field
            if query[0][0] == 1:
                return True
            return False
        except IndexError:
            return False
