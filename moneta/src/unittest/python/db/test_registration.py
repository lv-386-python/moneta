import unittest
from unittest import mock

import nose.tools as nt
from MySQLdb._exceptions import IntegrityError

from src.python.db import registration


class RegistrationTest(unittest.TestCase):
    """
    Class for testing user settings.
    """

    @mock.patch('src.python.db.registration.Registration._make_transaction')
    def test_save_data_integrity_error(self, mock_make_transaction):
        """
        Test "save_data" method with Integrity error.
        """
        kwargs = dict(currency=1, active=0, password='dedec', email='123@gmail.com')
        mock_make_transaction.side_effect = IntegrityError()
        result = registration.Registration.save_data(**kwargs)
        nt.assert_false(result)

    @mock.patch('src.python.db.user_settings.UserProfile._make_transaction')
    def test_save_data_successful_transaction(self, mock_make_transaction):
        """
        Test "save_data" method with successful transaction.
        """
        kwargs = dict(currency=1, active=0, password='dedec', email='123@gmail.com')
        mock_make_transaction.return_value = None
        result = registration.Registration.save_data(**kwargs)
        nt.assert_true(result)

    @mock.patch('src.python.db.registration.Registration._make_select')
    def test_email_exist_id_db_negative_result(self, mock_make_select):
        """
        Test "email_exist_id_db" method with negative result.
        """
        kwargs = dict(email='123@gmail.com')
        mock_make_select.return_value = []
        result = registration.Registration.save_data(**kwargs)
        nt.assert_false(result)

    @mock.patch('src.python.db.registration.Registration._make_select')
    def test_email_exist_id_db_positive_result(self, mock_make_select):
        """
        Test "email_exist_id_db" method with negative result.
        """
        kwargs = dict(email='123@gmail.com')
        mock_make_select.return_value = True
        result = registration.Registration.save_data(**kwargs)
        nt.assert_true(result)

    @mock.patch('src.python.db.registration.Registration._make_select')
    def test_get_user_id_integrity_error(self, mock_make_select):
        """
        Test "get_user_id" method with Integrity error.
        """
        kwargs = dict(email='123@gmail.com')
        mock_make_select.side_effect = IntegrityError()
        result = registration.Registration.save_data(**kwargs)
        nt.assert_false(result)

    @mock.patch('src.python.db.registration.Registration._make_select')
    def test_get_user_id_successful_transaction(self, mock_make_select):
        """
        Test "get_user_id" method with Integrity error.
        """
        kwargs = dict(email='123@gmail.com')
        mock_make_select.return_value = True
        result = registration.Registration.save_data(**kwargs)
        nt.assert_true(result)

    @mock.patch('src.python.db.registration.Registration._make_select')
    def test_is_active_integrity_error(self, mock_make_select):
        """
        Test "is_active" method with Integrity error.
        """
        kwargs = dict(id_user=1)
        mock_make_select.side_effect = IntegrityError()
        result = registration.Registration.save_data(**kwargs)
        nt.assert_false(result)

    @mock.patch('src.python.db.registration.Registration._make_select')
    def test_is_active_negative_result(self, mock_make_select):
        """
        Test "is_active" method with negative result.
        """
        kwargs = dict(id_user=1)
        mock_make_select.return_value = False
        result = registration.Registration.save_data(**kwargs)
        nt.assert_true(result)

    @mock.patch('src.python.db.registration.Registration._make_select')
    def test_is_active_positive_result(self, mock_make_select):
        """
        Test "is_active" method with positive result.
        """
        kwargs = dict(id_user=1)
        mock_make_select.return_value = True
        result = registration.Registration.save_data(**kwargs)
        nt.assert_true(result)

    @mock.patch('src.python.db.registration.Registration._make_transaction')
    def test_confirm_user_integrity_error(self, mock_make_transaction):
        """
        Test "confirm_user" method with Integrity error.
        """
        kwargs = dict(id_user=1)
        mock_make_transaction.side_effect = IntegrityError()
        result = registration.Registration.save_data(**kwargs)
        nt.assert_false(result)

    @mock.patch('src.python.db.registration.Registration._make_transaction')
    def test_confirm_user_successful_transaction(self, mock_make_transaction):
        """
        Test "confirm_user" method with successful transaction.
        """
        kwargs = dict(id_user=1)
        mock_make_transaction.return_value = []
        result = registration.Registration.save_data(**kwargs)
        nt.assert_true(result)





