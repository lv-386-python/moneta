"""This module provides API functionality for Redis."""
import redis


class RedisWorker():
    """Class for interaction with Redis db"""
    def __init__(self):
        """Open redis connection vial poll manager"""
        redis_pool = redis.ConnectionPool(host='localhost', port=6379)
        self.__redis = redis.Redis(connection_pool=redis_pool)

    def __enter__(self):
        """Return redis connection"""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Close Redis connection"""
        self.__redis.connection_pool.disconnect()


    def set(self, key, value, expiration=None):
        """
        Set new key:value pair in Redis with expiration time.
        expiration in seconds i.e. 15 min = 900
        Return True in case of success, else return False
        """
        try:
            self.__redis.set(key, value, expiration)
        except redis.RedisError:
            return False

        return True

    def get(self, key):
        """
        Get value from Redis, by given key.
        return it in bytes type.
        """
        try:
            response = self.__redis.get(key)
            value = response.decode('utf-8') if response else None
        except redis.RedisError:
            value = None

        return value

    def delete(self, key):
        """
        Delete key:value pair from redis db by given key.
        Return True in case of success, else return False
        """
        try:
            self.__redis.delete(key)
        except redis.RedisError:
            return False

        return True


__all__ = ['RedisWorker']
