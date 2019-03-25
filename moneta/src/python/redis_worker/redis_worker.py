"This module provides API functionality for Redis."

from redis import Redis, RedisError

from redis_configuration import REDIS_HOST, REDIS_PORT, REDIS_PASSWORD


def singleton(class_):
    ' Function for singleton pattern realisation '
    instances = {}

    def getinstance(*args, **kwargs):
        'chek for existance'
        if class_ not in instances:
            instances[class_] = class_(*args, **kwargs)
        return instances[class_]

    return getinstance


@singleton
class RedisWorker():
    'Class for interactin with Redis db'
    __redis = Redis(host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD)

    def set(self, key, value, expiration=None):
        """
        Set new key:value pair in Redis with expiration time.
        expiration in seconds i.e. 15 min = 900
        """
        try:
            self.__redis.set(key, value, expiration)
        except RedisError:
            return False

        return True

    def get(self, key):
        """
        return value from Redis, by given key.
        return in Bytes type.
        """
        try:
            value = self.__redis.get(key)
        except RedisError:
            value = None

        return value

# TODO unit tests