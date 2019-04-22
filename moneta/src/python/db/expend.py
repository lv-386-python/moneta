# coding=utf-8
"""Module for manipulation data regarding Expend instance.."""

from datetime import datetime

from core.db.db_helper import DbHelper
from core.utils import get_logger

# Get an instance of a LOGGER
LOGGER = get_logger(__name__)


class Expend(DbHelper):
    """
    Model for manipulation data regarding Expend instance.
    """

    @staticmethod
    def get_last_expend():
        """Getting last expend from database."""
        query = """
            SELECT id from expend
            WHERE mod_time = (SELECT MAX(mod_time) FROM expend);"""
        return Expend._make_select(query, ())

    @staticmethod
    def create_expend(name, currency, amount, image_id, owner_id):
        """Creating new expend"""
        create_time = datetime.now().timestamp()
        mod_time = create_time
        query = """
            INSERT INTO expend (name, currency, create_time, mod_time, amount, image_id, owner_id)
            VALUES (%s, %s, %s, %s, %s, %s, %s);"""
        args = (name, currency, create_time, mod_time, amount, image_id, owner_id)
        Expend._make_transaction(query, args)

    @staticmethod
    def create_user_expend(user_id):
        """Creating new record in user_expend table."""
        query = """
            INSERT INTO user_expend (user_id, expend_id, can_edit)
            VALUES (%s, %s, %s)"""
        expend_id = Expend.get_last_expend()[0]['id']
        can_edit = 1
        args = (user_id, expend_id, can_edit)
        Expend._make_transaction(query, args)

    @staticmethod
    def get_default_currencies():
        """Getting all available currencies from database."""
        query = """SELECT currency from currencies;"""
        currencies = Expend._make_select(query, ())
        result = []
        for i in range(len(currencies)):
            result += currencies[i].values()
        return tuple(enumerate(result))

    @staticmethod
    def get_expend_list_by_user_id(user_id):
        """
        Gets a list of expends for a logged user.
        :params: user_id - id of logged user
        :return: list of expends
        """
        sql = """
            SELECT
                e.id, e.name, cs.currency,
                e.mod_time, e.amount,
                i.css, user_expend.can_edit
            FROM user_expend
            LEFT JOIN expend e ON user_expend.expend_id = e.id
            LEFT JOIN image i ON e.image_id = i.id
            LEFT JOIN currencies cs ON e.currency = cs.id
            WHERE user_expend.user_id=%s
            ORDER BY e.name;
            """
        args = (user_id,)
        query = Expend._make_select(sql, args)
        return query
