from db.current import Current
from db.expend import Expend
from db.transaction_manager import Transaction


class CurrentValidators(Current):
    @staticmethod
    def is_user_valide(email):
        """
        Gets a current by id for a logged user.
        :params: email: check if user with this email exist in db
        :return: id email exist
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
        Gets a current by id for a logged user.
        :params: email: check if user with this email exist in db
        :return: id email exist
        """
        users = list(x['user_id'] for x in CurrentValidators.get_users_list_by_current_id(current_id))
        if user_id in users:
            return True
        return False

    @staticmethod
    def is_user_can_share(user, current_id):
        """
        Gets a current by id for a logged user.
        :params: email: check if user with this email exist in db
        :return: id email exist
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
        Gets a current by id for a logged user.
        :params: email: check if user with this email exist in db
        :return: id email exist
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
        if not type(unshare_id) == int:
            return False
        if len(str(unshare_id)) > 11:
            return False
        return True


class ExpendValidators(Expend):
    @staticmethod
    def is_user_valide(email):
        """
        Gets a expend by id for a logged user.
        :params: email: check if user with this email exist in db
        :return: id email exist
        """

        sql = """
                select id from auth_user where email=%s;
                """
        id_user = ExpendValidators._make_select(sql, (email,))
        if id_user:
            return id_user[0]['id']
        return False

    @staticmethod
    def is_already_share_validator(expend_id, user_id):
        """
        Gets a expend by id for a logged user.
        :params: email: check if user with this email exist in db
        :return: id email exist
        """
        users = list(x['user_id'] for x in ExpendValidators.get_users_list_by_expend_id(expend_id))
        if user_id in users:
            return True
        return False

    @staticmethod
    def is_user_can_share(user, expend_id):
        """
        Gets a expend by id for a logged user.
        :params: email: check if user with this email exist in db
        :return: id email exist
        """
        sql = """
              select owner_id from expend where id=%s;
              """
        owner = int(ExpendValidators._make_select(sql, (expend_id,))[0]['owner_id'])
        if user.id == owner:
            return True
        return False

    @staticmethod
    def is_user_can_unshare(user, expend_id, cancel_share_id):
        """
        Gets a expend by id for a logged user.
        :params: email: check if user with this email exist in db
        :return: id email exist
        """

        sql = """
                select owner_id from expend where id=%s;
                """
        owner_id = ExpendValidators._make_select(sql, (expend_id,))[0]['owner_id']
        if (user.id == owner_id or user.id == cancel_share_id) and (owner_id != cancel_share_id):
            return True
        return False

    @staticmethod
    def is_unshare_id_valid(unshare_id):
        if not type(unshare_id) == int:
            return False
        if len(str(unshare_id)) > 11:
            return False
        return True


class TransactionValidators(Transaction):
    @staticmethod
    def can_user_make_transaction(data, user):
        """

        """
        query = """
                select user_id from user_{tf} 
                where {tf}_id = {from_id} and user_id in 
                (select user_id from user_{tt} where {tt}_id = {to_id});
                """.format(tf=data['type_from'],
                           from_id=data['id_from'],
                           tt=data['type_to'],
                           to_id=data['id_to']
                           )
        permited_users = [x['user_id'] for x in TransactionValidators._make_select(query, ())]
        if user in permited_users:
            return True
        return False

    @staticmethod
    def data_is_valid(data):
        """

        """
        keys = ['type_from', 'id_from', 'id_to', 'amount_from', 'amount_to', 'type_to']
        types = [['income', 'current'], ['current', 'current'], ['current', 'expend']]
        for i in keys:
            if i not in data.keys():
                return False
        if [data['type_from'], data['type_to']] not in types:
            return False
        # if type(data['id_from']) != str or type(data['id_to']) != str:
        #     return False
        return True

