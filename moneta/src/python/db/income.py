"""
Module for interaction with income table in a database.
"""
from core import decorators, utils  # pylint:disable = import-error, no-name-in-module
from core.db import pool_manager as db # pylint:disable = import-error, no-name-in-module
from core.db.db_helper import DbHelper

class Income(DbHelper):

    @staticmethod
    @decorators.retry_request()
    def update_income_in_db(income_id, name, amount, image_id):
        """
        Update an income table in a database.
        :params: user_id - id of logged user, income_id - id of edited income,
                 name - new name for income, mod_time - modification time,
                 image_id - image for income
        :return: True if success, else False
        """
        sql = f"""
                UPDATE income
                SET name=%s, amount=%s, image_id = %s
                WHERE income.id=%s;
                """
        args = (name, amount, image_id, income_id)
        try:
            Income._make_transaction(sql, args)
        except IntegrityError:
            return False
        return True

    @staticmethod
    @decorators.retry_request()
    def delete_income(income_id):
        """
        Deletes an income field in a database.
        :params: income_id - id of income.
        :return: True if success, else False
        """
        sql = f"""
            DELETE FROM income
            WHERE id=%s;
            """
        args = (income_id,)
        try:
            Income._make_transaction(sql, args)
        except IntegrityError:
            return False
        return True

    @staticmethod
    @decorators.retry_request()
    def get_income_list_by_user_id(user_id):
        """
        Gets a list of incomes for a logged user.
        :params: user_id - id of logged user
        :return: list of currents
        """
        sql = f"""
            SELECT
                income.id, income.name, income.currency,
                income.mod_time, income.amount, image.css
            FROM income 
            JOIN image ON income.image_id = image.id
            WHERE income.user_id=%s
            ORDER BY income.name;
            """
        args = (user_id, )
        try:
            with db.DBPoolManager().get_connect() as connect:
                cursor = connect.cursor()
                cursor.execute(sql, args)
                sql_str = cursor.fetchall()
                row = [item for item in sql_str]
        except IntegrityError:
            return None
        return row


    @staticmethod
    @decorators.retry_request()
    def get_income(user_id, income_id):
        """
        Gets a list of incomes for a logged user.
        :params: user_id - id of logged user
        :return: list of currents
        """
        sql = f"""
            SELECT
                income.id, income.name, income.currency,
                income.mod_time, income.amount, image.css
            FROM income
            JOIN image ON income.image_id = image.id
            WHERE income.user_id=%s and income.id=%s
            ORDER BY income.name;
            """
        args = (user_id, income_id,)
        try:
            with db.DBPoolManager().get_connect() as connect:
                cursor = connect.cursor()
                cursor.execute(sql, args)
                sql_str = cursor.fetchall()
                row = sql_str[0]
        except IntegrityError:
            return None
        return row
