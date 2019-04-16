from datetime import datetime

from core.db.db_helper import DbHelper


class Income(DbHelper):
    '''
    Model for manipulation data regarding Income instance.
    '''

    # @staticmethod
    # def get_last_income():
    #     query = """SELECT id FROM income WHERE mod_time=(SELECT MAX(mod_time) FROM income);"""
    #     return Income._make_select(query, ())

    @staticmethod
    def create(name, currency, amount, image_id, user_id):
        create_time = datetime.now().timestamp()
        mod_time = create_time
        query = """  
                        INSERT INTO income (name, currency, user_id, create_time, mod_time, amount, image_id)
                        VALUES (%s, %s, %s, %s, %s, %s, %s);   
                    """

        args = (name, currency, user_id, create_time, mod_time, amount, image_id)
        Income._make_transaction(query, args)

    @staticmethod
    def get_default_currencies():
        query = """SHOW COLUMNS FROM user where Field='def_currency';"""

        currencies = Income._make_select(query, ())[0]['Type']
        def_currency = [item[1:-1] for item in currencies[5:-1].split(',')]
        return tuple(enumerate(def_currency))
