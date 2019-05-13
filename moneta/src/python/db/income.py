"""
Module for interaction with income table in a database.
"""
from datetime import datetime

from core import decorators # pylint:disable = import-error, no-name-in-module
from core.db.db_helper import DbHelper


class Income(DbHelper):
    '''
    Model for manipulation data regarding Income instance.
    '''

    @staticmethod
    def create(name, currency, amount, image_id, user_id, owner_id):
        """
                Update an income table in a database.
                :params: name - new name for income, currency - currency for income,
                         amount - amount of edited income, image_id - image for income,
                         user_id - id's of user
                :return: True if success, else False
                """
        create_time = datetime.now().timestamp()
        mod_time = create_time
        query = """
                   INSERT INTO income (name, currency, user_id, create_time, mod_time, amount, image_id, owner_id)
                   VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
                   """

        args = (name, currency, user_id, create_time, mod_time, amount, image_id, owner_id)
        Income._make_transaction(query, args)

    @staticmethod
    @decorators.retry_request()
    def update_income_in_db(income_id, name, image_id, mod_time):
        """
        Update an income table in a database.
        :params: income_id - id of edited income, name - new name for income,
                 amount - amount of edited income, image_id - image for income
        :return: True if success, else False
        """
        sql = """
                UPDATE income
                SET name=%s,  image_id = %s, mod_time = %s
                WHERE income.id=%s;
                """
        args = (name, image_id, mod_time, income_id)
        Income._make_transaction(sql, args)

    @staticmethod
    @decorators.retry_request()
    def delete_income(income_id):
        """
        Deletes an income field in a database.
        :params: income_id - id of income.
        :return: True if success, else False
        """
        sql = """
            DELETE FROM income
            WHERE id=%s;
            """
        args = (income_id,)
        Income._make_transaction(sql, args)

    @staticmethod
    @decorators.retry_request()
    def get_income_list_by_user_id(user_id):
        """
        Gets a list of incomes by user id.
        :params: user_id - id of logged user
        :return: list of incomes
        """
        sql = """
            SELECT
                income.id, income.name, cs.currency,
                income.mod_time, income.amount, image.css
            FROM income
            LEFT JOIN image ON income.image_id = image.id
            LEFT JOIN currencies cs ON income.currency = cs.id
            WHERE income.user_id=%s
            ORDER BY income.name;
            """
        args = (user_id,)
        query = Income._make_select(sql, args)
        return query

    @staticmethod
    @decorators.retry_request()
    def get_info_income(user_id, income_id):
        """
        Gets a detailed information of incomes for a logged user.
        :params: user_id - id of logged user, income_id - id of edited income
        :return: list of incomes
        """
        sql = """
            SELECT
                income.id, income.name, currencies.currency,
                income.mod_time, income.amount, image.css
            FROM income
            JOIN image ON income.image_id = image.id
            JOIN currencies ON income.currency = currencies.id
            WHERE income.user_id=%s and income.id=%s
            ORDER BY income.name;
            """
        args = (user_id, income_id,)
        query = Income._make_select(sql, args)
        if query:
            return query[0]
        return None
