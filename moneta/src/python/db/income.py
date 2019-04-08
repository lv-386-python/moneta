from datetime import datetime

import core.db.pool_manager as dbm


class Income:
    '''
    Model for manipulation data regarding Expend instance.
    '''

    def __init__(self, name, currency, image_id):
        '''Initiation fields of an Expend istance.'''
        self.name = name
        self.currency = currency
        self.image_id = image_id
        self.create_time = datetime.now().timestamp()

    def create(self):
        with dbm.DBPoolManager().get_cursor() as curs:
            query = f"""
                        INSERT INTO income (name, currency, create_time, image_id)
                        VALUES ('{self.name}', '{self.currency}',
                        '{self.create_time}', '{self.image_id}');
                    """

            curs.execute(query)
            return curs.fetchall()
