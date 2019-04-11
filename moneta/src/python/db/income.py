"""
Module for interaction with income table in a database.
"""
from core import decorators, utils  # pylint:disable = import-error, no-name-in-module
from core.db import pool_manager as db # pylint:disable = import-error, no-name-in-module

class Income():

    # @staticmethod
    # @decorators.retry_request()
    # def update_income_in_db(income_id, name, mod_time, image_id):  # pylint: disable=unused-argument
    #     """
    #     Update an income table in a database.
    #     :params: user_id - id of logged user, income_id - id of edited income,
    #              name - new name for income, mod_time - modification time,
    #              image_id - image for income
    #     :return: True if success, else False
    #     """
    #     query = f"""
    #             UPDATE income
    #             SET name='{name}', mod_time={mod_time}, image_id={image_id}
    #             WHERE income.id={income_id};
    #             """
    #     args = (name, mod_time, image_id, income_id)
    #     with db.DBPoolManager().get_connect() as connect:
    #         cursor = connect.cursor()
    #         cursor.execute(query, args)


    # @staticmethod
    # def delete_income(user_id, income_id):
    #     """
    #     Deletes an income field in a database.
    #     :params: user_id - id of logged user, income_id - id of income,
    #     :return: True if success, else False
    #     """
    #     sql = f"""
    #         DELETE FROM user_income
    #         WHERE income_id=%s AND user_id=%s;
    #         """
    #     args = (income_id, user_id)
    #     with db.DBPoolManager().get_connect() as connect:
    #         cursor = connect.cursor()
    #         cursor.execute(query, args)

    @staticmethod
    def get_income_list_by_user_id(user_id):
        """
        Gets a list of incomes for a logged user.
        :params: user_id - id of logged user
        :return: list of currents
        """
        sql = f"""
            SELECT
                income.id, income.name, income.currency,
                income.mod_time, income.amount
            FROM income
            WHERE income.user_id=%s
            ORDER BY income.name;
            """
        args = (user_id, )
        with db.DBPoolManager().get_connect() as connect:
            cursor = connect.cursor()
            cursor.execute(sql, args)
            sql_str = cursor.fetchall()
            count = cursor.rowcount
        print(count)
        for i in range(count):
            name = str(sql_str[i-1][1])
            currency = sql_str[i-1][2]
            amount = float(sql_str[i-1][4])
            sqllist = [name,currency,amount]
            print(name, currency, amount)
        return sqllist

    # @staticmethod
    # def can_edit_income(user_id, income_id):
    #     """
    #     Returns True if user can edit an income, else returns False.
    #     :params: user_id - id of logged user, income_id - id of income
    #     :return: True or False
    #     """
    #     sql = f"""
    #         SELECT can_edit
    #         FROM  user_income
    #         WHERE user_id=%s AND income_id=%s;
    #         """
    #     args = (user_id, income_id)
    #     with db.DBPoolManager().get_connect() as connect:
    #         cursor = connect.cursor()
    #         cursor.execute(sql, args)
    #         sql_str = cursor.fetchall()
    #     if not sql_str:
    #         return None
    #     return sql_str
    #
    #
