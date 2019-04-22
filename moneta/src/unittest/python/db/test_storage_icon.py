import unittest
from unittest import mock

import nose.tools as nt

from src.python.db import storage_icon


class StorageIconTest(unittest.TestCase):
    """
    Class for testing StorageIcon.
    """

    @mock.patch('src.python.db.storage_icon.StorageIcon._make_select')
    def test_get_icons(self, mock_make_select):
        """
        Test "get_icons" method.
        """
        kwargs = dict(category='current')
        mock_make_select.return_value = True
        result = storage_icon.StorageIcon.get_icons(**kwargs)
        nt.assert_true(result)

    @mock.patch('src.python.db.storage_icon.StorageIcon.get_icons')
    def test_get_icon_choices_by_category_type_error(self, mock_get_icons):
        """
        Test "get_icon_choices_by_category" method with TypeError.
        """
        kwargs = dict(category='current')
        mock_get_icons.return_value = None
        result = storage_icon.StorageIcon.get_icon_choices_by_category(**kwargs)
        nt.assert_equal(result, None)

    @mock.patch('src.python.db.storage_icon.StorageIcon.get_icons')
    def test_get_icon_choices_by_category_success(self, mock_get_icons):
        """
        Test "get_icon_choices_by_category" method with success.
        """
        kwargs = dict(category='current')
        mock_get_icons.return_value = (
            {'id': 1, 'css': 'coins', 'category': 'current'},
            {'id': 2, 'css': 'coin-9', 'category': 'current'})
        result = storage_icon.StorageIcon.get_icon_choices_by_category(**kwargs)
        nt.assert_equal(result, (('1', 'coins'), ('2', 'coin-9')))
