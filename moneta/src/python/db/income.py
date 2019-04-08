from core.db import pool_manager as db # pylint:disable = import-error, no-name-in-module

class Income():

    @staticmethod
    def edit_current(user_id, income_id, name, mod_time, image_id):  # pylint: disable=unused-argument
        """
        Edits a current table in a database.
        :params: user_id - id of logged user, income_id - id of edited current,
                 name - new name for current, mod_time - modification time,
                 image_id - image for current
        :return: True if success, else False
        """
        sql = f"""
                UPDATE income 
                SET name='{name}', mod_time={mod_time}, image_id={image_id}
                WHERE current.id={current_id}; 
                """
        return True