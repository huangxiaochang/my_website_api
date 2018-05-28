from django.db import models

# Create your models here.
# 用户信息
class UserInfo(models.Model):
    password = models.CharField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    email = models.CharField(max_length=255, unique=True)
    register_time = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.name
    
    class Meta:
        db_table = 'api_user_info'
        verbose_name="用户"
        verbose_name_plural="用户"
 
# 用户注册确认信息
class ConfirmInfo(models.Model):
    code = models.CharField(max_length=255)
    email = models.CharField(max_length=255, unique=True)
    add_time = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.email
    
    class Meta:
        db_table = 'api_confirm_info'
        ordering = ["-add_time"]
        verbose_name="确认码"
        verbose_name_plural="确认码"
        