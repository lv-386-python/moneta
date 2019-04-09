from datetime import datetime

from django.db import models

import core.db.pool_manager as dbm
from db.storage_icon import StorageIcon


class Income:
    '''
    Model for manipulation data regarding Expend instance.
    '''

    @staticmethod
    def get_default_currencies():
        query = """SHOW COLUMNS FROM user where Field='def_currency';"""
        with dbm.DBPoolManager().get_connect() as conn:
            cursor = conn.cursor()
            cursor.execute(query)
            currencies = cursor.fetchall()[0][1]
            def_currency = [item[1:-1] for item in currencies[5:-1].split(',')]
        return tuple(enumerate(def_currency))

    # name = models.CharField()
    # currency = models.CharField(choices=get_default_currencies())
    # amount = models.CharField()
    # image = models.CharField(choices=StorageIcon.get_icon_choices_by_category("income"))

    @staticmethod
    def create(name, currency, amount, image):
        with dbm.DBPoolManager().get_cursor() as curs:
            create_time = datetime.now().timestamp()
            query = f"""  
                        INSERT INTO income (name, currency, amount, create_time, image)
                        VALUES (%s, %s,%s,%s,%s );
                    """
            args = (name, currency, amount, create_time, image)
            curs.execute(query, args)
        return curs.fetchone()
