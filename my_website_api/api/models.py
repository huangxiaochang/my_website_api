from django.db import models

# Create your models here.

class UserInfo(models.Model):
    password = models.CharField(max_length=255)
    account_name = models.CharField(max_length=255)
    user_emit = models.CharField(max_length=64)

    class Meta:
        db_table = 'api_user_info'