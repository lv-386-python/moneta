"This module provide tests for core"
import unittest

import nose

from src.python.core.db.redis_worker import RedisWorker


class TestRedisWorker(unittest.TestCase):
    "Test for Redis worker"
    _redis = RedisWorker()

    def test_set(self):
        "unittest set function"
        case_1 = self._redis.set('test_key_1', 'some@mail.com', 30)
        nose.tools.ok_(case_1, msg=None)
        case_2 = self._redis.set('test_key_1', 'another@mail_to_the_same_key.com', 30)
        nose.tools.ok_(case_2, msg=None)

    def test_get(self):
        "unittest get function"
        self._redis.set('test_key_3', 'test_value', 60)
        case_1 = self._redis.get('test_key_3')
        nose.tools.eq_(case_1, 'test_value', msg=None)

    def test_delete(self):
        "unittest delete function"
        case_1 = self._redis.delete('test_key_3')
        nose.tools.ok_(case_1, msg=None)


if __name__ == '__main__':
    nose.main()
