
from utils import pool_manager as db


@db.re_request()
def find_user_in_database(our_user):
    try:
        query = f"Select * from user where email = '{our_user}'"
        with db.pool_manage().manage() as connect:
            cursor = connect.cursor()
            cursor.execute(query)
            sql_str = cursor.fetchall()  # make a list from sets
    except (ValueError, IntegrityError):
        pass
    if not sql_str:
        return None
    else:
        return our_user

@db.re_request()
def save_password_in_db(our_user, new_password):
    try:
        changed_password = f"UPDATE user SET password = '{new_password}' WHERE email = '{our_user}'"
        with db.pool_manage().manage() as connect:
            cursor = connect.cursor()
            cursor.execute(changed_password)
    except:
        pass
    return new_password



