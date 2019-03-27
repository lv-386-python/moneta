# -*- coding: utf-8 -*-
import random
import time
from threading import Thread
from MySQLdb import _mysql
from queue import Queue
import time
import logging
logging.basicConfig(filename='pool.log', filemode="w", level=logging.DEBUG)

class FullPullManager(Exception):
    pass


def singleton(_cls):
    instances = {}

    def get_instance(*args, **kwargs):
        if _cls not in instances:
            instances[_cls] = _cls(*args, **kwargs)
        return instances[_cls]

    return get_instance


class ConnectionToDB(Thread):
    """
    A threading example
    """
    def __init__(self, configurations, query, queue, pool_number):
        """Инициализация потока"""
        
        Thread.__init__(self)
        self.queue = queue
        self.config = configurations
        self.query = query
        self.pool_number = pool_number

    def send_queris(self):
        self.connection.query(self.query)
        r = self.connection.store_result()
        self.queue.put((self.pool_number, r.fetch_row(0)))

    def run(self):
        self.connection = _mysql.connect(**self.config)
        self.send_queris()
        self.connection.close()


@singleton
class DBPoolManager():

    MAX_POOL = 5
    pool = 0
    queue = Queue()

    @classmethod
    def sendquery(cls, configurations, query):
        rez = False
        if cls.pool < cls.MAX_POOL:
            cls.pool += 1
            pool_num = cls.pool
            connect = ConnectionToDB(configurations, query, cls.queue, pool_num)
            # logging.info(pool_num)
            connect.start()
            cls.pool -= 1
            while not rez:
                if cls.queue.empty():
                    continue
                rez = cls.queue.get()
                if rez[0] != pool_num:
                    cls.queue.put(rez)
                    rez = False
            logging.info(rez)
            return rez
        else:
            raise FullPullManager   
                

class TypouUser(Thread):
    def __init__(self):
        """Инициализация потока"""
        Thread.__init__(self)
        self.a = {'user' : 'wm_139',
         'passwd' : '254789631_QaSz',
         'host' : 'localhost',
         'port' : 3306,
         'db' : 'soft_serve_test'
        }
    
        self.query = """select NAME from USER where NAME = "MAN1";"""

    def run(self):
        manager = DBPoolManager()
        i = 0
        while i < 100:
            try:
                manager.sendquery(self.a, self.query)
                logging.info('+')
                i+=1
            except FullPullManager:
                logging.error('FullPullManager')
                continue 


def create_threads():
    for i in range(150):
        user = TypouUser()
        user.start()


if __name__ == "__main__":
    
    create_threads()
