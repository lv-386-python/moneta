import MySQLdb

DB_USER = 'moneta_user'
DB_NAME = 'db_moneta'
DB_PASS = 'db_password'


class UserRegistration:

    @staticmethod
    def execute_query(query):
        CONNECTION = MySQLdb.connect(user=DB_USER, passwd=DB_PASS, db=DB_NAME)
        cursor = CONNECTION.cursor()
        try:
            cursor.execute(query)
            CONNECTION.commit()
        except Exception:
            print('EROR')
            raise
            CONNECTION.rollback()
        CONNECTION.close()

    @staticmethod
    def save_user(email, password, def_currency):
        query_user = f"INSERT INTO auth_user (password, email) " \
                f"VALUE ('{password}', '{email}')"
        query_currency = f"INSERT INTO user (def_currency, is_active) VALUE ('{def_currency}', '1')"
        UserRegistration.execute_query(query_user)
        UserRegistration.execute_query(query_currency)

    @staticmethod
    def user_already_exists(email):
        CONNECTION = MySQLdb.connect(user=DB_USER, passwd=DB_PASS, db=DB_NAME)
        cursor = CONNECTION.cursor()
        select_email = f'SELECT * FROM user WHERE email = "{email}";'
        with cursor:
            cursor.execute(select_email)
            exists_email = cursor.fetchone()
        return bool(exists_email)
