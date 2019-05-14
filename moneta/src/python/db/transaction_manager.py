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

    @staticmethod
    def get_current_transaction(current_id):
        query = """select f.name as from_name, t.name as to_name, 
                   main.amount_to as amount_change, main.create_time 
                   from income_to_current as main 
                   left join income as f 
                   on main.from_income_id = f.id 
                   left join current as t 
                   on main.to_current_id = t.id 
                   where main.to_current_id = 5
                   UNION
                   select f.name as from_name, t.name as to_name, 
                   main.amount_from as amount_change, main.create_time 
                   from current_to_current as main 
                   left join current as f 
                   on main.from_current_id = f.id 
                   left join current as t 
                   on main.to_current_id = t.id 
                   where from_current_id = 5
                   UNION
                   select f.name as from_name, t.name as to_name, 
                   main.amount_to as amount_change, main.create_time 
                   from current_to_current as main 
                   left join current as f 
                   on main.from_current_id = f.id 
                   left join current as t 
                   on main.to_current_id = t.id 
                   where to_current_id = 5
                   UNION
                   select f.name as from_name, t.name as to_name, 
                   main.amount_from as amount_change, main.create_time 
                   from current_to_expend as main 
                   left join current as f 
                   on main.from_current_id = f.id 
                   left join expend as t 
                   on main.to_expend_id = t.id 
                   where main.from_current_id = 5
                   order by create_time;
                   """.format(current_id)
        data = Transaction._make_select(query, ())
        return data

    @staticmethod
    def get_income_transaction(income_id):
        query = """select f.name as name_from, t.name as name_to, main.amount_from, main.amount_to, main.create_time 
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
        query = """select f.name as name_from, t.name as name_to, main.amount_from, main.amount_to, main.create_time 
                   from current_to_expend as main 
                   left join current as f 
                   on main.from_current_id = f.id 
                   left join expend as t 
                   on main.to_expend_id = t.id 
                   where main.to_expend_id = {}
                   order by create_time;""".format(expend_id)
        data = Transaction._make_select(query, ())
        return data
