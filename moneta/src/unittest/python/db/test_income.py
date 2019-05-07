from contextlib import contextmanager

import nose

import db.income as inc

mock_db = []
DictCursor = True

class MockConection:
    class _cursor():
        @staticmethod
        def execute(query, args=()):
            record = (query, args)
            mock_db.append(record)

        @staticmethod
        def fetchall():
            return tuple(mock_db)

    @staticmethod
    def cursor(is_cursore=False):
        if is_cursore:
            pass
        return MockConection._cursor


class MockPollManager:
    @staticmethod
    @contextmanager
    def get_cursor():
        yield MockConection.cursor()

    @staticmethod
    @contextmanager
    def get_connect():
        yield MockConection()


class TestIncome:
    def setUp(self):
        '''setup function'''
        self.save_me_please = inc.DBPoolManager
        inc.DBPoolManager = MockPollManager

    def tearDown(self):
        '''tearDown function'''
        inc.DBPoolManager = self.save_me_please

    def test_execute_query(self):
        inc.DbHelper()._Expend__execute_query('some query', (1, 2))
        assert mock_db[-1] == ('some query', (1, 2))

    def test___get_from_db(self):
        res = inc.DbHelper._Expend__get_from_db('query', ('some', 'args'))
        assert res == tuple(mock_db)

    def test_get_expend_by_id(self):
        res = inc.DbHelper().get_expend_by_id(1)
        assert res == mock_db[0]


if __name__ == '__main__':
    nose.main()
