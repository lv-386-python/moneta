from datetime import datetime

import core.db.pool_manager as dbm


# from MySQLdb.cursors import DictCursor


class Income:
    '''
    Model for manipulation data regarding Income instance.
    '''

    @staticmethod
    def execute_query(query, args):
        '''Connecting to database and executing query.'''
        with dbm.DBPoolManager().get_cursor() as curs:
            # Execute the SQL command
            curs.execute(query, args)

    @staticmethod
    def get_from_db(query):
        with dbm.DBPoolManager().get_connect() as conn:
            cursor = conn.cursor()
            cursor.execute(query)
            result = cursor.fetchall()
        return result

    @staticmethod
    def get_last_income():
        query = """SELECT id FROM income WHERE mod_time=(SELECT MAX(mod_time) FROM income);"""
        return Income.get_from_db(query=query)

    @staticmethod
    def create(name, currency, user_id, amount, image_id):
        create_time = datetime.now().timestamp()
        mod_time = create_time
        query1 = """  
                        INSERT INTO income (name, currency, create_time, mod_time, amount, image_id)
                        VALUES (%s, %s, %s, %s, %s, %s);   
                    """
        query2 = """  
                                INSERT INTO user_income (user_id, income_id, can_edit) VALUES (%s, %s, %s);     

                            """

        args1 = (name, currency, create_time, mod_time, amount, image_id)
        Income.execute_query(query=query1, args=args1)
        # print(Income.execute_query(query=query1, args=args1))
        can_edit = 1
        income_id = Income.get_last_income()[0]['id']
        args2 = (user_id, income_id, can_edit)
        Income.execute_query(query=query2, args=args2)

    @staticmethod
    def get_default_currencies():
        query = """SHOW COLUMNS FROM user where Field='def_currency';"""

        currencies = Income.get_from_db(query)[0][1]
        def_currency = [item[1:-1] for item in currencies[5:-1].split(',')]
        return tuple(enumerate(def_currency))
