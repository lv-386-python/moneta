import nose

import unittest.mock as mock

from db.expend import Expend


class MockPolmanager:
    pass


class MockConection:

    mock_db = []
    def _cursor(self,query,args=()):
        record = (query, args)
        self.mock_db.append(record)

    def __init__(self):
        self.cursor = self._cursor

@mock.patch('core.db.poolmanager.py')
def test_edit_name():
    pass






