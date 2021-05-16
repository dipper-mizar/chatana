from django.db import models


class Users(models.Model):
    name = models.CharField(max_length=20, verbose_name="name")
    password = models.CharField(max_length=20, verbose_name="password")
    status = models.BooleanField(default=False, verbose_name="status")