"This module contain decorators for singleton and retrying run of some function"
import functools
import time


class RetryError(Exception):
    """Exception \"of ending try counter\""""


def retry_request(counter=5, wait_time=1):
    " Decorator for resendings requests to the DB "
    def retry_request_wrapper(func):
        @functools.wraps(func)
        def inner(*args, **kwargs):
            wr_counter, wait = counter, wait_time
            while wr_counter:
                try:
                    return func(*args, **kwargs)
                except Exception: # pylint:disable = broad-except
                    if wr_counter:
                        time.sleep(wait)
                    else:
                        raise RetryError
                wr_counter -= 1
        return inner
    return retry_request_wrapper


def singleton(_cls):
    " Function for singleton pattern realisation "
    instances = {}

    def get_instance(*args, **kwargs):
        if _cls not in instances:
            instances[_cls] = _cls(*args, **kwargs)
        return instances[_cls]

    return get_instance
