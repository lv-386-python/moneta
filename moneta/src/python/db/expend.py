from ..core.db.pool_manager import pool_manage


class Expend:
    '''
    Model for manipulation data regarding Expend instance.
    '''

    def __init__(self, expend_id, name, currency, image_id):
        '''Initiation fields of an Expend instance.'''
        self.id = expend_id
        self.name = name
        self.currency = currency
        self.image_id = image_id

    @staticmethod
    def execute_query(query):
        with pool_manage().transaction() as curs:
            curs.execute(query)

    @staticmethod
    def edit_name(expend_id, new_name):
        """method for renaming expend"""

        query = f"""
            UPDATE expend
            SET name = "{new_name}"
            WHERE id = {expend_id};"""
        Expend.execute_query(query)

    @staticmethod
    def edit_planned_cost(expend_id, new_planned_cost):
        """method for editting planned cost in expend"""
        query = f"""
                UPDATE expend
                SET planned_cost = {new_planned_cost}
                WHERE id = {expend_id}"""
        Expend.execute_query(query)

    @staticmethod
    def edit_image_id(expend_id, new_image_id):
        """method for editing image for expend"""
        query = f"""
                UPDATE expend
                SET image_id = {new_image_id}
                WHERE id = {expend_id};"""
        Expend.execute_query(query)

    @staticmethod
    def delete_user_to_expend(expend_id, user_id):
        query = f"""
                    DELETE FROM user_expend
                    WHERE user_id = {user_id} AND expend_id = {expend_id};"""
        Expend.execute_query(query)

    @staticmethod
    def get_expend_by_id(expend_id):
        query = f"SELECT * FROM expend WHERE id = {expend_id}"
        with pool_manage().manage() as conn:
            curs = conn.cursor()
            curs.execute(query)
            return curs.fetchone()
