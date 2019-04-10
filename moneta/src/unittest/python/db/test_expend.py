from contextlib import contextmanager

import nose

import db.expend as exp

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


class TestExpend:
    def setUp(self):
        '''setup function'''
        self.save_me_please = exp.DBPoolManager
        exp.DBPoolManager = MockPollManager

    def tearDown(self):
        '''tearDown function'''
        exp.DBPoolManager = self.save_me_please

    def test_execute_query(self):
        exp.Expend()._Expend__execute_query('some query', (1, 2))
        assert mock_db[-1] == ('some query', (1, 2))

    def test___get_from_db(self):
        res = exp.Expend._Expend__get_from_db('query', ('some', 'args'))
        assert res == tuple(mock_db)

    def test_edit_name(self):
        args = ('new', 1)
        query = 'UPDATE expend SET name = %s WHERE id = %s;'
        exp.Expend().edit_name(1, 'new')

        assert (query, args) == mock_db[-1]

    def test_edit_planned_cost(self):
        query = 'UPDATE expend SET amount = %s WHERE id = %s;'
        args = (200, 1,)
        exp.Expend().edit_amount(1, 200)

        assert (query, args) == mock_db[-1]

    def test_edit_image(self):
        query = 'UPDATE expend SET image_id = %s WHERE id = %s;'
        args = (2, 1)
        exp.Expend().edit_image_id(1, 2)

        assert (query, args) == mock_db[-1]

    def test_delete_expend_for_user(self):
        query = 'DELETE FROM user_expend WHERE expend_id = %s AND user_id = %s;'
        args = (1, 3)
        exp.Expend().delete_expend_for_user(1, 3)

        assert (query, args) == mock_db[-1]

    def test_get_expend_by_id(self):
        res = exp.Expend().get_expend_by_id(1)
        assert res == mock_db[0]


if __name__ == '__main__':
    nose.main()
