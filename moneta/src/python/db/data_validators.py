from db.current import Current
from db.expend import Expend


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
