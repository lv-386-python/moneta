import unittest
from unittest import mock

import nose.tools as nt
from MySQLdb._exceptions import IntegrityError

from src.python.db import current


class CurrentTest(unittest.TestCase):
    """
    Class for testing Current.
    """

    # TODO Vasyl # pylint: disable=fixme
    @mock.patch('src.python.db.current.Current._make_transaction')
    def test_create_current(self, mock_make_transaction):
        """
        Test "create_current" method.
        """
        mock_make_transaction.return_value = True
        result = current.Current.create_current()
        nt.assert_true(result)

    @mock.patch('src.python.db.current.Current._make_transaction')
    def test_edit_current_integrity_error(self, mock_make_transaction):
        """
        Test "edit_current" method with IntegrityError.
        """
        kwargs = dict(user_id=1, current_id=1, name="bank", mod_time=1554579944, image_id=5)
        mock_make_transaction.side_effect = IntegrityError()
        result = current.Current.edit_current(**kwargs)
        nt.assert_false(result)

    @mock.patch('src.python.db.current.Current._make_transaction')
    def test_edit_current_successful_transaction(self, mock_make_transaction):
        """
        Test "edit_current" method with successful transaction.
        """
        kwargs = dict(user_id=1, current_id=1, name="bank", mod_time=1554579944, image_id=5)
        mock_make_transaction.return_value = None
        result = current.Current.edit_current(**kwargs)
        nt.assert_true(result)

    @mock.patch('src.python.db.current.Current._make_transaction')
    def test_delete_current_integrity_error(self, mock_make_transaction):
        """
        Test "delete_current" method with IntegrityError.
        """
        kwargs = dict(user_id=1, current_id=1)

        mock_make_transaction.side_effect = IntegrityError()
        result = current.Current.delete_current(**kwargs)
        nt.assert_false(result)

    @mock.patch('src.python.db.current.Current._make_transaction')
    def test_delete_current_successful_transaction(self, mock_make_transaction):
        """
        Test "delete_current" with successful transaction.
        """
        kwargs = dict(user_id=1, current_id=1)

        mock_make_transaction.return_value = None
        result = current.Current.delete_current(**kwargs)
        nt.assert_true(result)

    @mock.patch('src.python.db.current.Current._make_select')
    def test_get_current_list_by_user_id(self, mock_select):
        """
        Test "get_current_list_by_user_id" method.
        """
        kwargs = dict(user_id=1)

        mock_select.return_value = True
        result = current.Current.get_current_list_by_user_id(**kwargs)
        nt.assert_equal(result, True)

    @mock.patch('src.python.db.current.Current._make_select')
    def test_get_current_by_id(self, mock_select):
        """
        Test "get_current_by_id" method.
        """
        kwargs = dict(user_id=1, current_id=1)

        mock_select.return_value = ['first', 'second']

        result = current.Current.get_current_by_id(**kwargs)
        nt.assert_equal(result, 'first')

    @mock.patch('src.python.db.current.Current._make_select')
    def test_can_edit_current_index_error(self, mock_select):
        """
        Test "can_edit_current" method with IndexError.
        """
        kwargs = dict(user_id=1, current_id=1)

        mock_select.return_value = []
        result = current.Current.can_edit_current(**kwargs)
        nt.assert_false(result)

    @mock.patch('src.python.db.current.Current._make_select')
    def test_can_edit_current_positive_result(self, mock_select):
        """
        Test "can_edit_current" method with positive result.
        """
        kwargs = dict(user_id=1, current_id=1)

        mock_select.return_value = [{'can_edit': 1}, {'can_edit': 0}]
        result = current.Current.can_edit_current(**kwargs)
        nt.assert_true(result)

    @mock.patch('src.python.db.current.Current._make_select')
    def test_can_edit_current_negative_result(self, mock_select):
        """
        Test "can_edit_current" method with negative result.
        """
        kwargs = dict(user_id=1, current_id=1)

        mock_select.return_value = [{'can_edit': 0}, {'can_edit': 0}]
        result = current.Current.can_edit_current(**kwargs)
        nt.assert_false(result)
