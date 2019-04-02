import MySQLdb

class User:

    def __init__(self, email, def_currency, password):
        self.email = email
        self.def_currency = def_currency
        self.password = password

    @staticmethod
    def query_user(query):
        CONNECTION = MySQLdb.connect(user='moneta_user', passw='db_password', db='db_moneta')
        cursor = CONNECTION.cursor()
        try:
            cursor.execute(query)
            CONNECTION.commit()
        except Exception:
            CONNECTION.rollback()
        CONNECTION.close()

    @staticmethod
    def create_user(email, def_currency, password):
        CONNECTION = MySQLdb.connect(user='moneta_user', passw='db_password', db='db_moneta')
        cursor = CONNECTION.cursor()
        user_exists = """SELECT email FROM user"""
        if int(user_exists) > 0:
            return
        with cursor:
            cursor.execute('SELECT max(id) from user;')
            user_id = cursor.fetchall() + 1;
        query = f"""INSERT INTO user(id, email, def_currency, password)
                    VALUE ('{user_id}','{email}', '{def_currency}', '{password}')"""
        User.query_user(query)