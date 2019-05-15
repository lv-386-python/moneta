""" This module provides transaction interface and execute 3 query for making transactions
"""
import time

from decimal import Decimal
from core.db.db_helper import DbHelper


class Transaction(DbHelper):  # pylint:disable = too-few-public-methods
    """
    Class for making transactions in database
    """

    @staticmethod
    def get_transaction_from_table(table, id):
        query = """select * from {} 
                       where id = {}
                       """.format(table, id)
        data = Transaction._make_select(query, ())
        return data

    @staticmethod
    def make_transaction(data, user_id):
        """
        :param data: dict of data from view, must contain all
        information about all sides of transaction
        """
        transaction_time = int(time.time())
        query = """
                INSERT INTO {fr}_to_{t}(from_{fr}_id, to_{t}_id, amount_from, amount_to, create_time, user_id)
                VALUES({id_from}, {id_to}, {amount_from}, {amount_to}, {transaction_time}, {user_id});

                UPDATE {t}
                SET amount = amount + {amount_to}
                WHERE id = {id_to};
                """.format(fr=data['type_from'],
                           t=data['type_to'],
                           id_from=data['id_from'],
                           id_to=data['id_to'],
                           amount_from=(Decimal(data['amount_from'])),
                           amount_to=(Decimal(data['amount_to'])),
                           user_id=user_id,
                           transaction_time=transaction_time)
        if data['type_from'] == 'current':
            query += """
                     UPDATE current
                     SET amount = amount - {amount_from}
                     WHERE id = {id_from};
                     """.format(amount_from=(Decimal(data['amount_from'])),
                                id_from=data['id_from'])
        Transaction._make_transaction(query, ())

    @staticmethod
    def cancel_transaction(data, user_id):
        """
        :param data: dict of data from view, must contain all
        information about all sides of transaction
        """
        trans = Transaction.get_transaction_from_table(data['type'], data['id'])[0]
        type_from = data['type'][0:data['type'].find('_')]
        type_to = data['type'][data['type'].rfind('_')+1:]
        t_data = {'type_from': type_from,
                  'type_to': type_to,
                  'id_from': trans[f'from_{type_from}_id'],
                  'id_to': trans[f'to_{type_to}_id'],
                  'amount_from': -trans['amount_from'],
                  'amount_to': -trans['amount_to']}
        Transaction.make_transaction(t_data, user_id)

    @staticmethod
    def get_current_transaction(current_id):
        query = """select ('income_to_current') as type, main.id, 
                   f.name as name_from, t.name as name_to, 
                   main.amount_to as amount_change, main.create_time
                   from income_to_current as main 
                   left join income as f 
                   on main.from_income_id = f.id 
                   left join current as t 
                   on main.to_current_id = t.id 
                   where main.to_current_id = {0}
                   UNION
                   select ('current_to_current') as type, main.id, 
                   f.name as name_from, t.name as name_to, 
                   main.amount_from as amount_change, main.create_time
                   from current_to_current as main 
                   left join current as f 
                   on main.from_current_id = f.id 
                   left join current as t 
                   on main.to_current_id = t.id 
                   where from_current_id = {0}
                   UNION
                   select ('current_to_current') as type, main.id,
                   f.name as name_from, t.name as name_to, 
                   main.amount_to as amount_change, main.create_time
                   from current_to_current as main 
                   left join current as f 
                   on main.from_current_id = f.id 
                   left join current as t 
                   on main.to_current_id = t.id 
                   where to_current_id = {0}
                   UNION
                   select ('current_to_expend') as type, main.id, 
                   f.name as name_from, t.name as name_to, 
                   main.amount_from as amount_change, main.create_time
                   from current_to_expend as main 
                   left join current as f 
                   on main.from_current_id = f.id 
                   left join expend as t 
                   on main.to_expend_id = t.id 
                   where main.from_current_id = {0}
                   order by create_time;
                   """.format(current_id)
        data = Transaction._make_select(query, ())
        return data

    @staticmethod
    def get_income_transaction(income_id):
        query = """select ('income_to_current') as type, main.id,
                   f.name as name_from, t.name as name_to, 
                   main.amount_to as amount_change, main.create_time
                   from income_to_current as main 
                   left join income as f 
                   on main.from_income_id = f.id 
                   left join current as t 
                   on main.to_current_id = t.id 
                   where main.from_income_id = {}
                   order by create_time;""".format(income_id)
        data = Transaction._make_select(query, ())
        return data

    @staticmethod
    def get_expend_transaction(expend_id):
        query = """select ('current_to_expend') as type, main.id,
                   f.name as name_from, t.name as name_to,
                   main.amount_to as amount_change, main.create_time
                   from current_to_expend as main 
                   left join current as f 
                   on main.from_current_id = f.id 
                   left join expend as t 
                   on main.to_expend_id = t.id 
                   where main.to_expend_id = {}
                   order by create_time;""".format(expend_id)
        data = Transaction._make_select(query, ())
        return data
