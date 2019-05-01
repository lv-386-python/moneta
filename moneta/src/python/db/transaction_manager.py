""" This module provides transaction interface and execute 3 query for making transactions
"""
import time
from ast import literal_eval
from decimal import Decimal
from core.db.db_helper import DbHelper


class Transaction(DbHelper):  # pylint:disable = too-few-public-methods
    """
    Class for making transactions in database
    """

    @staticmethod
    def make_transaction(data):
        """
        Transaction manager
        :param data: dict of data from view, must contain all
        information about all sides of transaction
        """
        data['from'] = literal_eval(data['from'])
        data['to'] = literal_eval(data['to'])
        transaction_time = int(time.time())

        query = """
                INSERT INTO {fr}_to_{t}(from_{fr}_id, to_{t}_id, amount_from, amount_to, create_time, user_id)
                VALUES({id_from}, {id_to}, {amount_from}, {amount_to}, {transaction_time}, {user_id});
                
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
                           transaction_time=transaction_time)

        if data['from']['type'] == 'current':
            query += """
                     UPDATE current
                     SET amount = amount - {amount_from}
                     WHERE id = {id_from};
                     """.format(amount_from=abs(Decimal(data['amount_from'])),
                                id_from=data['from']['id'])

        Transaction._make_transaction(query, ())
