from django.db import models

class Change_password(models.Model):
    old_password_field = models.CharField(max_length=20)
    new_password_field = models.CharField(max_length=20)
    new_password_confirming_field = models.CharField(max_length=20)


# Create your models here.
