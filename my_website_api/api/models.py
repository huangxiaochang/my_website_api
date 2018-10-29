from django.db import models

# Create your models here.
# 定义文件存放的路径的函数,当然也可以使用django的形式： 如： upload_to = 'avatar/%Y/%m/%d/'
# 让上传的文件的路径动态地与user的名字相关
from my_website_api.settings import MEDIA_ROOT

# 用户信息
class UserInfo(models.Model):
    password = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    email = models.CharField(max_length=255, unique=True)
    register_time = models.DateTimeField(auto_now_add=True)
    avatar_url = models.CharField(max_length=255, null=True)
    role = models.CharField(max_length=255, default='admin')
    operate_permission = models.CharField(max_length=255, default='look')
    update_time = models.DateTimeField(null=True)

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
    update_time = models.DateTimeField(auto_now_add=True)
    is_success = models.BooleanField(default=False)

    def __str__(self):
        return self.email
    
    class Meta:
        db_table = 'api_confirm_info'
        ordering = ["-update_time"]
        verbose_name="确认码"
        verbose_name_plural="确认码"
        