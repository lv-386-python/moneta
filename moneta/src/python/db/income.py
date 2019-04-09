from core.db import pool_manager as db # pylint:disable = import-error, no-name-in-module

class Income():

    @staticmethod
    @decorators.retry_request()
    def update_income_in_db(user_id, income_id, name, mod_time, image_id):  # pylint: disable=unused-argument
        """
        Update an income table in a database.
        :params: user_id - id of logged user, income_id - id of edited income,
                 name - new name for income, mod_time - modification time,
                 image_id - image for income
        :return: True if success, else False
        """
        query = f"""
                UPDATE income 
                SET name='{name}', mod_time={mod_time}, image_id={image_id}
                WHERE income.id={current_id}; 
                """
        with db.DBPoolManager().get_connect() as connect:
            cursor = connect.cursor()
            cursor.execute(query)
        return True


    @staticmethod
