""" This module provides transaction interface and execute 3 query for making transactions
"""
import datetime
from ast import literal_eval
from decimal import Decimal
from core.db.db_helper import DbHelper


class Transaction(DbHelper):
    """
    Class for making transactions in database
    """

    @staticmethod
    def get_amount(current_id):
        """
        :param current_id: id of some current
        :return: decimal amount of some current
        """
        query = """
                SELECT amount 
                FROM current
                WHERE id = %s;
                """
        return Decimal(Transaction._make_select(query, (current_id, ))[0]['amount'])

    @staticmethod
    def make_transaction(data):
        """
        Transaction manager
        :param data: dict of data from view, must contain all
        information about all sides of transaction
        :raise: if data is invalid, or there are some erors raise Exception
        """
        data['from'] = literal_eval(data['from'])
        data['to'] = literal_eval(data['to'])
        transaction_time = datetime.datetime.now().timestamp()
        if data['from']['type'] == 'current':
            symbol = '-'
            amount_now = Transaction.get_amount(data['from']['id'])
            if Decimal(data['amount_from']) > amount_now:
                data['amount_from'] = amount_now
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
                           amount_from=abs(Decimal(data['amount_from'])),
                           amount_to=abs(Decimal(data['amount_to'])),
                           user_id=data['user_id'],
                           symbol=symbol,
                           transaction_time=transaction_time)

        try:
            Transaction._make_transaction(query, ())
        except Exception:
            raise Exception
