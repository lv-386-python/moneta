import MySQLdb

DB_USER = 'moneta_user'
DB_NAME = 'db_moneta'
DB_PASS = 'db_password'

class UserRegistration:

    def __init__(self, uid, email, password, def_currency):
        self.uid = uid
        self.password = password
        self.def_currency = def_currency
        self.email = email

    @staticmethod
    def execute_query(query):
        CONNECTION = MySQLdb.connect(user=DB_USER, passwd=DB_PASS, db=DB_NAME)
        cursor = CONNECTION.cursor()
        try:
            cursor.execute(query)
            CONNECTION.commit()
        except Exception:
            CONNECTION.rollback()
        CONNECTION.close()


    @staticmethod
    def save_user(email, password, def_currency):
        CONNECTION = MySQLdb.connect(user=DB_USER, passwd=DB_PASS, db=DB_NAME)
        cursor = CONNECTION.cursor()
        with cursor:
            cursor.execute("SELECT max(id) FROM user")
            uid = cursor.fetchall()[0][0] + 1
        query = f"INSERT INTO user (id, password, def_currency, email, is_activated) " \
            f"VALUE ({uid},'{password}', '{def_currency}', '{email}', '1')"
        UserRegistration.execute_query(query)

    # @staticmethod
    # def already_exists_user(email):
    #     CONNECTION = MySQLdb.connect(user=DB_USER, passwd=DB_PASS, db=DB_NAME)
    #     cursor = CONNECTION.cursor()
    #     with cursor:
    #         cursor.execute(f"SELECT * FROM user WHERE email = {email}")
    #         email = cursor.fetchall()

















    #
    # email = models.EmailField
    # password = models.CharField
    # def_current = models.CharField
    #
    # USERNAME_FIELD = 'email'
    # object = BaseUserManager()
    #
    # @staticmethod
    # def create_user(email, password, def_currency):
    #     user = UserRegistration()
    #     user.email = email
    #     user.set_password(password)
    #     user.def_currency = def_currency
    #     try:
    #         user.save()
    #         return user
    #     except (ValueError, IntegrityError):
    #         pass
