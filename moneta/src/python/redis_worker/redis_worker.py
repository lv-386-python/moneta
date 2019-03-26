"This module provides API functionality for Redis."

from redis import Redis, RedisError

from redis_credentials import REDIS_HOST, REDIS_PORT, REDIS_PASSWORD


def singleton(_cls):
    ' Function for singleton pattern realisation '
    instances = {}

    def get_instance(*args, **kwargs):
        if _cls not in instances:
            instances[_cls] = _cls(*args, **kwargs)
        return instances[_cls]

    return get_instance


@singleton
class RedisWorker():
    'Class for interaction with Redis db'
    __redis = Redis(host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD)

    def set(self, key, value, expiration=None):
        """
        Set new key:value pair in Redis with expiration time.
        expiration in seconds i.e. 15 min = 900
        Return True in case of success, else return False
        """
        try:
            self.__redis.set(key, value, expiration)
        except RedisError:
            return False

        return True

    def get(self, key):
        """
        return value from Redis, by given key.
        return in str type.
        """
        try:
            response = self.__redis.get(key)
            value = response.decode('utf-8')
        except RedisError:
            value = None

        return value

    def delete(self, key):
        '''
        Delete key:value pair from redis db by given key.
        Return True in case of success, else return False
        '''
        try:
            self.__redis.delete(key)
        except RedisError:
            return False

        return True
