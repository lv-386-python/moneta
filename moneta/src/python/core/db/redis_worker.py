"This module provides API functionality for Redis."

from redis import Redis, RedisError

REDIS_HOST = 'localhost'
REDIS_PORT = 6379



class RedisWorker():
    "Class for interaction with Redis db"

    def __enter__(self):
        "open a Redis connection and return it"
        print('enter')
        self.__redis = Redis(host=REDIS_HOST, port=REDIS_PORT)
        return self.__redis

    def __exit__(self, exc_type, exc_val, exc_tb):
        "close Redis conection and "

        self.__redis.connection_pool.disconnect()
        del self.__redis
        print('exit')

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
        return in bytes type.
        """
        try:
            response = self.__redis.get(key)
            value = response.decode('utf-8')
        except RedisError:
            value = None

        return value

    def delete(self, key):
        """
        Delete key:value pair from redis db by given key.
        Return True in case of success, else return False
        """
        try:
            self.__redis.delete(key)
        except RedisError:
            return False

        return True


__all__ = ['RedisWorker']


if __name__ == '__main__':
    with RedisWorker() as r:
        r.set('new', 'val', 15)
        res = r.get('new')
        print(res)
        print(r)

    print('hi', r)
