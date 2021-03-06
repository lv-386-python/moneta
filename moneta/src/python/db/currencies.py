"""
Module for working with currencies in a database.
"""

import json
from datetime import datetime, timedelta

from MySQLdb._mysql import IntegrityError
from django.core.serializers.json import DjangoJSONEncoder

import requests

from core.db.db_helper import DbHelper
from core.db.redis_worker import RedisWorker

JSON_API = "https://bank.gov.ua/NBUStatService/v1/statdirectory/exchange"
UAH_DEFAULT_RATE = 1
HTTP_OK_STATUS = 200
CURRENCY_CODE_IN_JSON = 'cc'


class Currency(DbHelper):
    """
    Model for working with currencies in a database.
    """

    @staticmethod
    def currency_list(dict_format=None):
        """
        Gets currency list from database.
        :return: currency list.
        """
        sql = """
            SELECT id, currency
            FROM currencies c;
            """
        query_result = Currency._make_select(sql)
        if dict_format:
            return query_result
        list_currencies = [value for item in query_result for value in item.values()]
        iter_list = iter(list_currencies)
        list_of_tuples = list(zip(iter_list, iter_list))
        return list_of_tuples

    @staticmethod
    def get_cur_by_id(cur_id):
        """
        Getting currency from database by requested id.
        :params: id of requested currency
        :return: currency string.
        """
        sql = """
            SELECT currency
            FROM currencies
            WHERE id = %s;
            """
        args = (cur_id,)
        try:
            query_result = Currency._make_select(sql, args)
        except IntegrityError:
            return False
        return query_result[0]['currency']

    @staticmethod
    def get_currency_rates():
        """
        Returns dictionary with currency rates for a certain day.
        At first tries to get currency rates from redis.
        At second - connects to site, if API works.
        Else returns None.
        """

        with RedisWorker() as redis:
            currency_rates = redis.get('currency_rates')

        if currency_rates:
            return json.loads(currency_rates)

        request = requests.get(f"{JSON_API}?json")
        if request.status_code != HTTP_OK_STATUS:
            return "Service is temporarily unavailable."

        currency_list = [item[1] for item in Currency.currency_list()]
        currency_rates = {}.fromkeys(currency_list, UAH_DEFAULT_RATE)
        for item in request.json():
            if item[CURRENCY_CODE_IN_JSON] in currency_list:
                currency_rates[item[CURRENCY_CODE_IN_JSON]] = (item['rate'])
        now = datetime.now()
        tomorrow = datetime.now() + timedelta(days=1)
        time_to_currency_rate_change = tomorrow.replace(hour=18, minute=0, second=0) - now

        # calculate time to currency rates change in seconds
        timer = time_to_currency_rate_change.total_seconds() % (3600 * 24)

        # save currency_rates to redis
        with RedisWorker() as redis:
            currency_rates_json = json.dumps(
                currency_rates,
                cls=DjangoJSONEncoder,
                ensure_ascii=False)
            redis.set('currency_rates', currency_rates_json, int(timer))

        return currency_rates
