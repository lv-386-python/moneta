import unittest
from unittest import mock

import core.db.pool_manager as db
from core.db import db_helper


class DbHelperTest(unittest.TestCase):
    """
    Class for testing DbHelper.
    """

    def setUp(self):
        """ Setup function. """
        db.DBPoolManager = mock.MagicMock()

    def test_make_select2(self):
        """
        Test "_make_select" method2.
        """
        kwargs = dict(sql_query='query', args=(1, 2))
        db_helper.DbHelper._make_select(**kwargs)
        db.DBPoolManager().get_connect().__enter__().cursor().execute.assert_called_with('query', (1, 2))

    def test_make_transaction(self):
        """
        Test "_make_transaction" method.
        """
        kwargs = dict(sql_query='query', args=(1, 2))
        db_helper.DbHelper._make_transaction(**kwargs)
        db.DBPoolManager().get_cursor().__enter__().execute.assert_called_with('query', (1, 2))
