from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.db import IntegrityError, models


class MonetaUser(AbstractBaseUser):
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    USERNAME_FIELD = 'email'
    object = BaseUserManager()

    @staticmethod
    def create(email, password):
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
