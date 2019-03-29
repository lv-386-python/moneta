"Module for interaction with DB"

import MySQLdb



DB_NAME = 'db_moneta'
DB_USER = 'moneta_user'
DB_PASS = 'DeathRow$1991'



def update_db(query):
    "this method open cursor and make update query"
    CONNECTION = MySQLdb.connect(user=DB_USER, passwd=DB_PASS, db=DB_NAME)
    cursor = CONNECTION.cursor()
    try:
        # Execute the SQL command
        cursor.execute(query)
        # Commit your changes in the database
        CONNECTION.commit()
    except:
        # Rollback in case there is any error
        CONNECTION.rollback()
    CONNECTION.close()


def edit_name(expend_id, new_name):
    "method for rename expend"

    query = f"""
        UPDATE expend
        SET name = '{new_name}'
        WHERE id = {expend_id};"""

    update_db(query)


def edit_planned_cost(expend_id, new_planned_cost):
    "method for edit planned cost in expend"

    query = f"""
            UPDATE expend
            SET planned_cost = {new_planned_cost}
            WHERE id = {expend_id};"""

    update_db(query)

def edit_image_id(expend_id, new_image_id):
    "method for edit image for expend"

    query = f"""
            UPDATE expend
            SET image_id = {new_image_id}
            WHERE id = {expend_id};"""

    update_db(query)

