""" This module provides transaction interface and execute 3 query for making transactions
"""
import datetime
from ast import literal_eval
from core.db.pool_manager import DBPoolManager


def make_transaction(data):
    """
    Transaction manager
    :param data: dict of data from view, must contain all information about all sides of transaction
    :raise: if data is invalid, or there are some erors raise Exception
    """
    data['from'] = literal_eval(data['from'])
    data['to'] = literal_eval(data['to'])
    transaction_time = datetime.datetime.now().timestamp()
    if data['from']['type'] == 'current':
        symbol = '-'
    else:
        symbol = '+'

    query = """
            INSERT INTO {fr}_to_{t}(from_{fr}_id, to_{t}_id, amount_from, amount_to, create_time, user_id)
            VALUES({id_from}, {id_to}, {amount_from}, {amount_to}, {transaction_time}, {user_id});
            
            UPDATE {fr}
            SET amount = amount {symbol} {amount_from}
            WHERE id = {id_from};
            
            UPDATE {t}
            SET amount = amount + {amount_to}
            WHERE id = {id_to};
            """.format(fr=data['from']['type'],
                       t=data['to']['type'],
                       id_from=data['from']['id'],
                       id_to=data['to']['id'],
                       amount_from=abs(int(data['amount_from'])),
                       amount_to=abs(int(data['amount_to'])),
                       user_id=data['user_id'],
                       symbol=symbol,
                       transaction_time=transaction_time)

    with DBPoolManager().get_cursor() as cursor:
        try:
            cursor.execute(query)
        except Exception:
            raise Exception
