""" This module provides transaction interface and execute 3 query for making transactions
"""
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

    if data['from']['type'] == 'current':
        symbol = '-'
    else:
        symbol = '+'

    query = """
            INSERT INTO {fr}_to_{t}(from_{fr}_id, to_{t}_id, amount_from, amount_to, user_id)
            VALUES({id_from}, {id_to}, {amount_from}, {amount_to}, {user_id});
            
            UPDATE {fr}
            SET amount = amount {symbol} {amount_to}
            WHERE id = {id_from};
            
            UPDATE {t}
            SET amount = amount + {amount_to}
            WHERE id = {id_to};
            """.format(fr=data['from']['type'],
                       t=data['to']['type'],
                       id_from=data['from']['id'],
                       id_to=data['to']['id'],
                       amount_from=data['amount_from'],
                       amount_to=data['amount_to'],
                       user_id=data['user_id'],
                       symbol=symbol)

    with DBPoolManager().get_cursor() as cursor:
        try:
            cursor.execute(query)
        except Exception:
            raise Exception
