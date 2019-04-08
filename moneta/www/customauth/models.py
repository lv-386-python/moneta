"""Class for Moneta User."""
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.db import IntegrityError, models


class MonetaUser(AbstractBaseUser):
    """ Class for creating user for moneta."""
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    USERNAME_FIELD = 'email'
    object = BaseUserManager()

    @staticmethod
    def create(email, password):
        """ Create a user for moneta."""
        user = MonetaUser()
        user.email = email
        user.set_password(password)
        try:
            user.save()
            return user
        except (ValueError, IntegrityError):
            pass

    class Meta:
        db_table = "auth_user"
