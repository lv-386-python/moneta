import unittest
from datetime import date, datetime
from unittest import mock

import nose.tools as nt

from src.python.db import stat_inform


class StatisticTest(unittest.TestCase):
    """
    Class for testing of Statistic.
    """

    @mock.patch('src.python.db.stat_inform.Statistic._make_select')
    def test_get_default_currency(self, mock_make_select):
        """
        Test "get_default_currency" method.
        """
        kwargs = dict(user_id=1)
        # args = (user_id=1,)
        mock_make_select.return_value = ['EUR', ]
        result = stat_inform.Statistic.get_default_currency(**kwargs)
        nt.assert_equal(result, 'EUR')

    @mock.patch('src.python.db.stat_inform.Statistic.get_income_total_sum_for_period')
    @mock.patch('src.python.db.currencies.Currency.get_currency_rates')
    @mock.patch('src.python.db.stat_inform.Statistic.get_default_currency')
    @mock.patch('src.python.db.stat_inform.Statistic._make_select')
    def test_get_income_statistic_for_period(
            self, mock_make_select, mock_default_currency,
            mock_currency_rates, mock_income_total_sum_for_period
    ):
        """
        Test "get_income_statistic_for_period" method.
        """
        kwargs = dict(user_id=1, start=1, end=2)
        mock_make_select.return_value = None
        result = stat_inform.Statistic.get_income_statistic_for_period(**kwargs)
        nt.assert_equal(result, (None, 0))

        mock_make_select.return_value = (
            {'income_sum': 400.0, 'name': 'salary_1', 'currency': 'USD'},
            {'income_sum': 500.0, 'name': 'salary_2', 'currency': 'USD'}
        )
        mock_default_currency.return_value = {'currency': 'UAH'}
        mock_currency_rates.return_value = {'UAH': 1, 'USD': 27}
        mock_income_total_sum_for_period.return_value = {'inc_total_sum': 24300.0, 'currency': 'UAH'}
        result = stat_inform.Statistic.get_income_statistic_for_period(**kwargs)
        nt.assert_equal(
            result,
            (({'currency': 'UAH',
               'income_sum': 10800.0,
               'name': 'salary_1',
               'percentage': '44.44'},
              {'currency': 'UAH',
               'income_sum': 13500.0,
               'name': 'salary_2',
               'percentage': '55.56'}),
             {'currency': 'UAH', 'inc_total_sum': 24300.0})
        )

    @mock.patch('src.python.db.stat_inform.Statistic.get_expend_total_sum_for_period')
    @mock.patch('src.python.db.currencies.Currency.get_currency_rates')
    @mock.patch('src.python.db.stat_inform.Statistic.get_default_currency')
    @mock.patch('src.python.db.stat_inform.Statistic._make_select')
    def test_get_expend_statistic_for_period(
            self, mock_make_select, mock_default_currency,
            mock_currency_rates, mock_expend_total_sum_for_period
    ):
        """
        Test "get_expend_statistic_for_period" method.
        """
        kwargs = dict(user_id=1, start=1, end=2)
        mock_make_select.return_value = None
        result = stat_inform.Statistic.get_expend_statistic_for_period(**kwargs)
        nt.assert_equal(result, (None, 0))

        mock_make_select.return_value = (
            {'expend_sum': 14500.0, 'name': 'rent', 'currency': 'UAH'},
            {'expend_sum': 16700.0, 'name': 'utilities', 'currency': 'UAH'}
        )
        mock_default_currency.return_value = {'currency': 'UAH'}
        mock_currency_rates.return_value = {'UAH': 1, 'USD': 27}
        mock_expend_total_sum_for_period.return_value = {'exp_total_sum': 31200.0, 'currency': 'UAH'}
        result = stat_inform.Statistic.get_expend_statistic_for_period(**kwargs)
        nt.assert_equal(
            result,
            (({'currency': 'UAH',
               'expend_sum': 14500.0,
               'name': 'rent',
               'percentage': '46.47'},
              {'currency': 'UAH',
               'expend_sum': 16700.0,
               'name': 'utilities',
               'percentage': '53.53'}),
             {'currency': 'UAH', 'exp_total_sum': 31200.0})
        )

    @mock.patch('src.python.db.currencies.Currency.get_currency_rates')
    @mock.patch('src.python.db.stat_inform.Statistic.get_default_currency')
    @mock.patch('src.python.db.stat_inform.Statistic._make_select')
    def test_get_income_total_sum_for_period(
            self, mock_make_select, mock_default_currency,
            mock_currency_rates
    ):
        """
        Test "get_income_total_sum_for_period" method.
        """
        kwargs = dict(user_id=1, start=1, end=2)

        mock_make_select.return_value = (
            {'inc_total_sum': 400.0, 'name': 'salary_1', 'currency': 'USD'},
            {'inc_total_sum': 500.0, 'name': 'salary_2', 'currency': 'USD'}
        )
        mock_default_currency.return_value = {'currency': 'UAH'}
        mock_currency_rates.return_value = {'UAH': 1, 'USD': 27}
        result = stat_inform.Statistic.get_income_total_sum_for_period(**kwargs)
        nt.assert_equal(result, {'currency': 'UAH', 'inc_total_sum': 24300.0})

    @mock.patch('src.python.db.currencies.Currency.get_currency_rates')
    @mock.patch('src.python.db.stat_inform.Statistic.get_default_currency')
    @mock.patch('src.python.db.stat_inform.Statistic._make_select')
    def test_get_expend_total_sum_for_period(
            self, mock_make_select, mock_default_currency,
            mock_currency_rates
    ):
        """
        Test "get_expend_total_sum_for_period" method.
        """
        kwargs = dict(user_id=1, start=1, end=2)

        mock_make_select.return_value = (
            {'exp_total_sum': 500.0, 'name': 'rent', 'currency': 'USD'},
            {'exp_total_sum': 500.0, 'name': 'utilities', 'currency': 'USD'}
        )
        mock_default_currency.return_value = {'currency': 'UAH'}
        mock_currency_rates.return_value = {'UAH': 1, 'USD': 27}
        result = stat_inform.Statistic.get_expend_total_sum_for_period(**kwargs)
        nt.assert_equal(result, {'currency': 'UAH', 'exp_total_sum': 27000.0})

    def test_get_percentages(self):
        """
        Test "get_percentages" method.
        """
        kwargs = dict(
            sum_category="expend_sum",
            items=({'expend_sum': 14500.0, 'name': 'rent', 'currency': 'UAH'},
                   {'expend_sum': 16700.0, 'name': 'utilities', 'currency': 'UAH'}),
            total_sum=31200
        )
        result = stat_inform.Statistic.get_percentages(**kwargs)
        nt.assert_equal(
            result,
            ({'expend_sum': 14500.0, 'name': 'rent', 'currency': 'UAH', 'percentage': '46.47'},
             {'expend_sum': 16700.0, 'name': 'utilities', 'currency': 'UAH', 'percentage': '53.53'})
        )

    @mock.patch('src.python.db.stat_inform.Statistic.get_income_statistic_for_period')
    @mock.patch('src.python.db.stat_inform.Statistic.get_expend_statistic_for_period')
    def test_get_all_statistic_by_date(self, mock_expend_statistic, mock_income_statistic):
        """
        Test "get_all_statistic_by_date" method.
        """
        kwargs = dict(user_id=1, analyzed_date=date.today())
        mock_expend_statistic.return_value = (
            ({'expend_sum': 4900.0, 'name': 'other', 'currency': 'UAH', 'percentage': '100.00'},),
            {'exp_total_sum': 63100.0, 'currency': 'UAH'})
        mock_income_statistic.return_value = (
            ({'income_sum': 8200.0, 'name': 'other', 'currency': 'UAH', 'percentage': '100.00'},),
            {'inc_total_sum': 53700.0, 'currency': 'UAH'})

        result = stat_inform.Statistic.get_all_statistic_by_date(**kwargs)
        nt.assert_equal(
            result,
            {'year_exp_trans': ({'expend_sum': 4900.0, 'name': 'other', 'currency': 'UAH', 'percentage': '100.00'},),
             'year_inc_trans': ({'income_sum': 8200.0, 'name': 'other', 'currency': 'UAH', 'percentage': '100.00'},),
             'year_exp_total_sum': {'exp_total_sum': 63100.0, 'currency': 'UAH'},
             'year_inc_total_sum': {'inc_total_sum': 53700.0, 'currency': 'UAH'},
             'month_exp_trans': ({'expend_sum': 4900.0, 'name': 'other', 'currency': 'UAH', 'percentage': '100.00'},),
             'month_inc_trans': ({'income_sum': 8200.0, 'name': 'other', 'currency': 'UAH', 'percentage': '100.00'},),
             'month_exp_total_sum': {'exp_total_sum': 63100.0, 'currency': 'UAH'},
             'month_inc_total_sum': {'inc_total_sum': 53700.0, 'currency': 'UAH'},
             'date_for_output': {'year': 2019, 'month': 'May'}}
        )

    @mock.patch('src.python.db.stat_inform.Statistic.get_income_statistic_for_period')
    @mock.patch('src.python.db.stat_inform.Statistic.get_expend_statistic_for_period')
    def test_get_all_statistic_by_date(self, mock_expend_statistic, mock_income_statistic):
        """
        Test "get_all_statistic_by_date" method.
        """
        kwargs = dict(user_id=1, analyzed_date=datetime(2019, 5, 17))
        mock_expend_statistic.return_value = (
            ({'expend_sum': 4900.0, 'name': 'other', 'currency': 'UAH', 'percentage': '100.00'},),
            {'exp_total_sum': 63100.0, 'currency': 'UAH'})
        mock_income_statistic.return_value = (
            ({'income_sum': 8200.0, 'name': 'other', 'currency': 'UAH', 'percentage': '100.00'},),
            {'inc_total_sum': 53700.0, 'currency': 'UAH'})
        result = stat_inform.Statistic.get_all_statistic_by_date(**kwargs)
        nt.assert_equal(
            result,
            {'year_exp_trans': ({'expend_sum': 4900.0, 'name': 'other', 'currency': 'UAH', 'percentage': '100.00'},),
             'year_inc_trans': ({'income_sum': 8200.0, 'name': 'other', 'currency': 'UAH', 'percentage': '100.00'},),
             'year_exp_total_sum': {'exp_total_sum': 63100.0, 'currency': 'UAH'},
             'year_inc_total_sum': {'inc_total_sum': 53700.0, 'currency': 'UAH'},
             'month_exp_trans': ({'expend_sum': 4900.0, 'name': 'other', 'currency': 'UAH', 'percentage': '100.00'},),
             'month_inc_trans': ({'income_sum': 8200.0, 'name': 'other', 'currency': 'UAH', 'percentage': '100.00'},),
             'month_exp_total_sum': {'exp_total_sum': 63100.0, 'currency': 'UAH'},
             'month_inc_total_sum': {'inc_total_sum': 53700.0, 'currency': 'UAH'},
             'date_for_output': {'year': 2019, 'month': 'May'}}
        )

    @mock.patch('src.python.db.stat_inform.Statistic.get_income_statistic_for_period')
    @mock.patch('src.python.db.stat_inform.Statistic.get_expend_statistic_for_period')
    def test_get_statistic_by_period(self, mock_expend_statistic, mock_income_statistic):
        """
        Test "get_statistic_by_period" method.
        """
        kwargs = dict(user_id=1, period_begin=1, period_end=2)
        mock_expend_statistic.return_value = (
            ({'expend_sum': 4900.0, 'name': 'other', 'currency': 'UAH', 'percentage': '100.00'},),
            {'exp_total_sum': 63100.0, 'currency': 'UAH'})
        mock_income_statistic.return_value = (
            ({'income_sum': 8200.0, 'name': 'other', 'currency': 'UAH', 'percentage': '100.00'},),
            {'inc_total_sum': 53700.0, 'currency': 'UAH'})
        result = stat_inform.Statistic.get_statistic_by_period(**kwargs)
        nt.assert_equal(
            result,
            {'exp_trans': ({'expend_sum': 4900.0, 'name': 'other', 'currency': 'UAH', 'percentage': '100.00'},),
             'inc_trans': ({'income_sum': 8200.0, 'name': 'other', 'currency': 'UAH', 'percentage': '100.00'},),
             'exp_total_sum': {'exp_total_sum': 63100.0, 'currency': 'UAH'},
             'inc_total_sum': {'inc_total_sum': 53700.0, 'currency': 'UAH'}, 'period_begin': '01/01/1970',
             'period_end': '01/01/1970'}
        )


if __name__ == '__main__':
    unittest.main()
