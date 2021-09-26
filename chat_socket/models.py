from django.db import models


class ChatRecord(models.Model):
    username = models.CharField(max_length=20, verbose_name='username')
    text = models.CharField(max_length=100, verbose_name='text')
