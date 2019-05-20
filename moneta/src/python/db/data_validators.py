"""
Module for validate all data that connect with transactions
and sharing for current and expend
"""

from db.currencies import Currency
from db.current import Current
from db.expend import Expend
from db.storage_icon import StorageIcon
from db.transaction_manager import Transaction


class CurrentValidators(Current):
    """
    Class for validate current sharing
    """
    @staticmethod
    def is_user_valid(email):
        """
        Check in user email is valid and exist in DB
        :param email: email from check
        :return: True if user is exist or False if not
        """

        sql = """
                select id from auth_user where email=%s;
                """
        id_user = CurrentValidators._make_select(sql, (email,))
        if id_user:
            return id_user[0]['id']
        return False

    @staticmethod
    def is_already_share_validator(current_id, user_id):
        """
        Check if current(current id) already shared for user(user_id)
        :param current_id: current for check
        :param user_id: user for check
        :return: True, if already shared/ False, if no
        """
        users = list(x['user_id'] \
                     for x in CurrentValidators.get_users_list_by_current_id(current_id))
        if user_id in users:
            return True
        return False

    @staticmethod
    def is_user_can_share(user, current_id):
        """
        Check if user has permission for share current
        :param user: user, who what to share
        :param current_id: current, that user would like to share
        :return: True, if can shared/ False, if no
        """
        sql = """
              select owner_id from current where id=%s;
              """
        owner = int(CurrentValidators._make_select(sql, (current_id,))[0]['owner_id'])
        if user.id == owner:
            return True
        return False

    @staticmethod
    def is_user_can_unshare(user, current_id, cancel_share_id):
        """
        Check if user has permission for unshare current
        :param user:user, who what to unshare
        :param current_id: current, that user would like to usshare
        :param cancel_share_id: user, for whom what to unshare
        :return: True, if can unshared/ False, if no
        """

        sql = """
                select owner_id from current where id=%s;
                """
        owner_id = CurrentValidators._make_select(sql, (current_id,))[0]['owner_id']
        if (user.id == owner_id or user.id == cancel_share_id) and (owner_id != cancel_share_id):
            return True
        return False

    @staticmethod
    def is_unshare_id_valid(unshare_id):
        """
        Check if unshare data is walid
        :param unshare_id: if for check
        :return: True, if valid/ False, if no
        """
        if not type(unshare_id) == int:  # pylint:disable = C0123
            return False
        if len(str(unshare_id)) > 11:
            return False
        return True


class ExpendValidators(Expend):
    """
        Class for validate expend sharing
    """
    @staticmethod
    def is_user_valid(email):
        """
        Check in user email is valid and exist in DB
        :param email: email from check
        :return: True if user is exist or False if not
        """

        sql = """
                SELECT id FROM auth_user WHERE email=%s;
                """
        id_user = ExpendValidators._make_select(sql, (email,))
        if id_user:
            return id_user[0]['id']
        return False

    @staticmethod
    def is_already_share_validator(expend_id, user_id):
        """
        Check if expend(current id) already shared for user(user_id)
        :param expend_id: expend for check
        :param user_id: user for check
        :return: True, if already shared/ False, if no
        """
        users = list(x['user_id'] for x in ExpendValidators.get_users_list_by_expend_id(expend_id))
        if user_id in users:
            return True
        return False

    @staticmethod
    def is_user_can_share(user, expend_id):
        """
        Check if user has permission for share expend
        :param user: user, who what to share
        :param expend_id: current, that user would like to share
        :return: True, if can shared/ False, if no
        """
        sql = """
              SELECT owner_id FROM expend WHERE id=%s;
              """
        owner = int(ExpendValidators._make_select(sql, (expend_id,))[0]['owner_id'])
        if user.id == owner:
            return True
        return False

    @staticmethod
    def is_user_can_unshare(user, expend_id, cancel_share_id):
        """
        Check if user has permission for unshare expend
        :param user:user, who what to unshare
        :param expend_id: expend, that user would like to usshare
        :param cancel_share_id: user, for whom what to unshare
        :return: True, if can unshared/ False, if no
        """

        sql = """
                SELECT owner_id FROM expend WHERE id=%s;
                """
        owner_id = ExpendValidators._make_select(sql, (expend_id,))[0]['owner_id']
        if (user.id == owner_id or user.id == cancel_share_id) and (owner_id != cancel_share_id):
            return True
        return False

    @staticmethod
    def is_unshare_id_valid(unshare_id):
        """
        Check if unshare data is walid
        :param unshare_id: if for check
        :return: True, if valid/ False, if no
        """
        if not type(unshare_id) == int:  # pylint:disable = C0123
            return False
        if len(str(unshare_id)) > 11:
            return False
        return True

    @staticmethod
    def data_validation(data):
        """
        Check whether data from user is valid.
        If amount of data args(name, image, currency, amount)
        then validation for create, else for update
        :param data from user POST or PUT
        :return True, if valid/ False, if not
        """
        if len(data['name']) >= 45:
            return False
        if not StorageIcon.get_icon_by_id(int(data['image'])):
            return False
        # check what data to validate.
        if len(data) > 3:
            if data['id_currency'] not in range(len(Currency.currency_list('dict'))):
                return False
            if not 1e+11 > int(data['amount']) > 0:
                return False
        return True


class TransactionValidators(Transaction):
    """
    Class for validate transactions
    """
    @staticmethod
    def can_user_make_transaction(data, user):
        """
        Check if user can make transaction
        :param data: data with data_from and data_to from check
        :param user: user_id for check
        :return: True, if user can make this transaction/ False if no
        """
        if data['type_from'] == 'income':
            query = """
                    select user_id from income 
                    where id = {from_id} and user_id in 
                    (select user_id from user_current where current_id = {to_id});
                    """.format(from_id=data['id_from'],
                               to_id=data['id_to']
                               )
        else:
            query = """
                    select user_id from user_{tf} 
                    where {tf}_id = {from_id} and user_id in 
                    (select user_id from user_{tt} where {tt}_id = {to_id});
                    """.format(tf=data['type_from'],
                               from_id=data['id_from'],
                               tt=data['type_to'],
                               to_id=data['id_to']
                               )
        print(query)
        users = TransactionValidators._make_select(query, ())
        if not users:
            return False
        permited_users = [x['user_id'] for x in users]
        if user in permited_users:
            return True
        return False

    @staticmethod
    def data_is_valid(data):
        """
        Check if data for transaction is valid
        :param data: transaction data
        :return:True, if valid/ False if no
        """
        keys = ['type_from', 'id_from', 'id_to', 'amount_from', 'amount_to', 'type_to']
        types = [['income', 'current'], ['current', 'current'], ['current', 'expend']]
        for i in keys:
            if i not in data.keys():
                return False
        if [data['type_from'], data['type_to']] not in types:
            return False
        return True

    @staticmethod
    def can_get_current_transaction(user, current_id):
        """
        Check if user have permission to get all transactions
        for one of the "Current" instance
        :param user: user for check
        :param current_id: current_id for check
        :return: Truse, if user has permission/ false if no
        """
        query = """
                SELECT user_id FROM user_current WHERE current_id={}
                """.format(current_id)
        users = TransactionValidators._make_select(query, ())
        if not users:
            return False

        user_list = [x['user_id'] for x in users]
        if user in user_list:
            return True
        return False

    @staticmethod
    def can_get_income_transaction(user, income_id):
        """
        Check if user have permission to get all transactions
        for one of the "Income" instance
        :param user: user for check
        :param income_id: income_id for check
        :return: Truse, if user has permission/ false if no
        """
        query = """
                    select user_id from income where id={}
                    """.format(income_id)
        users = TransactionValidators._make_select(query, ())
        if not users:
            return False
        user_list = [x['user_id'] for x in users]
        if user in user_list:
            return True
        return False

    @staticmethod
    def can_get_expend_transaction(user, expend_id):
        """
        Check if user have permission to get all transactions
        for one of the "Expend" instance
        :param user: user for check
        :param expend_id: expend_id for check
        :return: Truse, if user has permission/ false if no
        """
        query = """
                    select user_id from user_expend where expend_id={}
                    """.format(expend_id)
        users = TransactionValidators._make_select(query, ())
        if not users:
            return False
        user_list = [x['user_id'] for x in users]
        if user in user_list:
            return True
        return False
