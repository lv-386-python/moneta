"""
Module for a statistic.
"""

from datetime import datetime

from core import utils
from core.db.db_helper import DbHelper
from src.python.db.currencies import Currency


class Statistic(DbHelper):
    """
    Model for working with statistical information.
    """

    @staticmethod
    def get_default_currency(user_id):
        """
        Gets default user currency.
        :param user_id:
        :return: default currency
        """
        sql = f"""
            SELECT currency
            FROM currencies c
            LEFT JOIN user_settings us ON c.id = us.def_currency
            WHERE us.id=%s;
            """
        args = (user_id,)
        query_result = Statistic._make_select(sql, args)[0]
        return query_result

    @staticmethod
    def get_income_statistic_for_period(user_id, start, end):
        """
        Get statistical information about incomes during a given period.
        :param user_id:
        :param start: begin of period
        :param end: end of period
        :return: list of amounts per income
        """

        sql = f"""
            SELECT
                SUM(ic.amount_from) as income_sum, i.name, c.currency
            FROM income_to_current ic
            LEFT JOIN income i ON ic.from_income_id = i.id
            LEFT JOIN currencies c ON i.currency = c.id
            WHERE ic.user_id=%s and ic.create_time BETWEEN %s AND %s
            GROUP BY i.id
            ORDER BY i.id;
            """
        args = (user_id, start, end)
        query_result = Statistic._make_select(sql, args)

        if not query_result:
            return None, 0

        def_currency = Statistic.get_default_currency(user_id)['currency']
        currency_rates = Currency.get_currency_rates()

        # calculate all costs in default currency
        for item in query_result:
            item['income_sum'] = (
                item['income_sum'] * currency_rates[item['currency']] /
                currency_rates[def_currency]
            )
            item['currency'] = def_currency

        total_sum = Statistic.get_income_total_sum_for_period(user_id, start, end)
        query_result = Statistic.get_percentages(
            'income_sum', query_result, total_sum['inc_total_sum']
        )
        return query_result, total_sum

    @staticmethod
    def get_expend_statistic_for_period(user_id, start, end):
        """
        Get statistical information about expends during a given period.
        :param user_id:
        :param start: begin of period
        :param end: end of period
        :return: list of amounts per expend
        """
        sql = f"""
            SELECT
                SUM(ce.amount_to) as expend_sum, e.name, c.currency
            FROM current_to_expend ce
            LEFT JOIN expend e ON ce.to_expend_id = e.id
            LEFT JOIN currencies c ON e.currency = c.id
            WHERE ce.user_id=%s and ce.create_time BETWEEN %s AND %s
            GROUP BY e.id
            ORDER BY e.id;
            """

        args = (user_id, start, end)
        query_result = Statistic._make_select(sql, args)

        if not query_result:
            return None, 0

        def_currency = Statistic.get_default_currency(user_id)['currency']

        currency_rates = Currency.get_currency_rates()

        # calculate all costs in default currency
        for item in query_result:
            item['expend_sum'] = (
                item['expend_sum'] * currency_rates[item['currency']] /
                currency_rates[def_currency]
            )
            item['currency'] = def_currency

        total_sum = Statistic.get_expend_total_sum_for_period(user_id, start, end)
        query_result = Statistic.get_percentages(
            'expend_sum', query_result, total_sum['exp_total_sum']
        )
        return query_result, total_sum

    @staticmethod
    def get_income_total_sum_for_period(user_id, start, end):
        """
        Get total sum for incomes during a given period.
        :param user_id:
        :param start: begin of period
        :param end: end of period
        :return: total income sum
        """

        sql = f"""
            SELECT
                SUM(ic.amount_from) as inc_total_sum, c.currency
            FROM income_to_current ic
            LEFT JOIN income i ON ic.from_income_id = i.id
            LEFT JOIN currencies c ON i.currency = c.id
            WHERE ic.user_id=%s and ic.create_time BETWEEN %s AND %s
            GROUP BY c.currency;
            """
        args = (user_id, start, end)
        query_result = Statistic._make_select(sql, args)
        def_currency = Statistic.get_default_currency(user_id)['currency']

        currency_rates = Currency.get_currency_rates()

        # calculate total sum in default currency
        inc_sum = 0
        for item in query_result:
            inc_sum += (
                item['inc_total_sum'] * currency_rates[item['currency']] /
                currency_rates[def_currency]
            )
        return {'inc_total_sum': inc_sum, 'currency': def_currency}

    @staticmethod
    def get_expend_total_sum_for_period(user_id, start, end):
        """
        Get total sum for expends during a given period.
        :param user_id:
        :param start: begin of period
        :param end: end of period
        :return: total expend sum
        """
        sql = f"""
            SELECT
                SUM(ce.amount_to) as exp_total_sum, c.currency
            FROM current_to_expend ce
            LEFT JOIN expend e ON ce.to_expend_id = e.id
            LEFT JOIN currencies c ON e.currency = c.id
            WHERE ce.user_id=%s and ce.create_time BETWEEN %s AND %s
            GROUP BY c.currency;
            """
        args = (user_id, start, end)
        query_result = Statistic._make_select(sql, args)

        def_currency = Statistic.get_default_currency(user_id)['currency']
        currency_rates = Currency.get_currency_rates()

        # calculate total sum in default currency
        exp_sum = 0
        for item in query_result:
            exp_sum += (
                item['exp_total_sum'] * currency_rates[item['currency']] /
                currency_rates[def_currency]
            )

        return {'exp_total_sum': exp_sum, 'currency': def_currency}

    @staticmethod
    def get_percentages(sum_category, items, total_sum):
        """
        Get percentage of items.
        :param sum_category: category (income or expend)
        :param items: wallet element
        :param total_sum: total sum for calculation
        :return: items with percentages
        """
        for item in items:
            # get percentage of each position
            item['percentage'] = "{0:.2f}".format(item[sum_category] / total_sum * 100)
        return items

    @staticmethod
    def get_all_statistic_by_date(user_id, analyzed_date):
        """
        Get all statistical information for incomes and expends.
        :param user_id:
        :param analyzed_date: date, for which we get statistical information
        :return: dict with all statistical information
        """

        # expend transactions and total sum per year
        year_exp_trans, year_exp_total_sum = Statistic.get_expend_statistic_for_period(
            user_id, *utils.get_year_range_by_date(analyzed_date)
        )

        # income transactions and total sum per year
        year_inc_trans, year_inc_total_sum = Statistic.get_income_statistic_for_period(
            user_id, *utils.get_year_range_by_date(analyzed_date)
        )

        # expend transactions and total sum per month
        month_exp_trans, month_exp_total_sum = Statistic.get_expend_statistic_for_period(
            user_id, *utils.get_month_range_by_date(analyzed_date)
        )

        # income transactions and total sum per month
        month_inc_trans, month_inc_total_sum = Statistic.get_income_statistic_for_period(
            user_id, *utils.get_month_range_by_date(analyzed_date)
        )

        statistic_data = {
            'year_exp_trans': year_exp_trans,
            'year_inc_trans': year_inc_trans,
            'year_exp_total_sum': year_exp_total_sum,
            'year_inc_total_sum': year_inc_total_sum,
            'month_exp_trans': month_exp_trans,
            'month_inc_trans': month_inc_trans,
            'month_exp_total_sum': month_exp_total_sum,
            'month_inc_total_sum': month_inc_total_sum,
            'date_for_output': {
                'year': analyzed_date.year,
                'month': analyzed_date.strftime('%B')
            }
        }

        return statistic_data

    @staticmethod
    def get_statistic_by_period(user_id, period_begin, period_end):
        """
        Get statistical information for incomes and expends during given period.
        :param user_id:
        :param period_begin:
        :param period_end:
        :return: dict with statistical information
        """
        period_begin = int(period_begin)
        period_end = int(period_end)

        # expend transactions and total sum during given period
        exp_trans, exp_total_sum = Statistic.get_expend_statistic_for_period(
            user_id, period_begin, period_end
        )

        # income transactions and total sum during given period
        inc_trans, inc_total_sum = Statistic.get_income_statistic_for_period(
            user_id, period_begin, period_end
        )

        statistic_data = {
            'exp_trans': exp_trans,
            'inc_trans': inc_trans,
            'exp_total_sum': exp_total_sum,
            'inc_total_sum': inc_total_sum,
            'period_begin': datetime.utcfromtimestamp(period_begin).strftime("%d/%m/%Y"),
            'period_end': datetime.utcfromtimestamp(period_end).strftime("%d/%m/%Y")
        }
        return statistic_data

__all__ = ['Statistic']
