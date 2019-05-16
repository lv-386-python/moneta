import unittest
from unittest import mock

import nose.tools as nt
from MySQLdb._exceptions import IntegrityError

from src.python.db import user_settings


class UserSettingsTest(unittest.TestCase):
    """
    Class for testing user settings.
    """

    @mock.patch('src.python.db.user_settings.UserProfile._make_transaction')
    def test_update_pass_integrity_error(self, mock_make_transaction):
        """
        Test "update_pass" method with Integrity error.
        """
        kwargs = dict(new_password='123456', id_user=1)
        mock_make_transaction.side_effect = IntegrityError()
        result = user_settings.UserProfile.update_pass(**kwargs)
        nt.assert_false(result)

    @mock.patch('src.python.db.user_settings.UserProfile._make_transaction')
    def test_update_pass_successful_transaction(self, mock_make_transaction):
        """
        Test "update_pass" method with Integrity error.
        """
        kwargs = dict(new_password='123456', id_user=1)
        mock_make_transaction.return_value = None
        result = user_settings.UserProfile.update_pass(**kwargs)
        nt.assert_true(result)

    @mock.patch('src.python.db.user_settings.UserProfile._make_transaction')
    def test_update_currency_integrity_error(self, mock_make_transaction):
        """
        Test "update_currency" method with Integrity error.
        """
        kwargs = dict(new_currency=3, id_user=1)
        mock_make_transaction.side_effect = IntegrityError()
        result = user_settings.UserProfile.update_currency(**kwargs)
        nt.assert_false(result)

    @mock.patch('src.python.db.user_settings.UserProfile._make_transaction')
    def test_update_currency_successful_transaction(self, mock_make_transaction):
        """
        Test "update_currency" method with Integrity error.
        """
        kwargs = dict(new_currency=3, id_user=1)
        mock_make_transaction.return_value = None
        result = user_settings.UserProfile.update_currency(**kwargs)
        nt.assert_true(result)

    @mock.patch('src.python.db.user_settings.UserProfile._make_transaction')
    def test_delete_user_integrity_error(self, mock_make_transaction):
        """
        Test "delete_user" method with Integrity error.
        """
        kwargs = dict(id_user=1)
        mock_make_transaction.side_effect = IntegrityError()
        result = user_settings.UserProfile.delete_user(**kwargs)
        nt.assert_false(result)

    @mock.patch('src.python.db.user_settings.UserProfile._make_transaction')
    def test_delete_user_successful_transaction(self, mock_make_transaction):
        """
        Test "delete_user" method with Integrity error.
        """
        kwargs = dict(id_user=1)
        mock_make_transaction.return_value = None
        result = user_settings.UserProfile.delete_user(**kwargs)
        nt.assert_true(result)

    @mock.patch('src.python.db.user_settings.UserProfile._make_select')
    def test_check_user_default_currency(self, mock_make_select):
        """
        Test "check_user_default_currency" method.
        """
        kwargs = dict(user_id=1)
        mock_make_select.return_value = ['EUR', ]
        result = user_settings.UserProfile.check_user_default_currency(**kwargs)
        nt.assert_equal(result, 'EUR')



