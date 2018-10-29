"""
WSGI config for my_website_api project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/howto/deployment/wsgi/
"""
# wsgi 不是服务器，也不是用于进程交互的api, 更不是真实的代码，而只是定义了的一个接口。目标是在web服务器和web
# 框架层之间提供一个通用的api标准，其应用是可调用的对象
import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "my_website_api.settings")

application = get_wsgi_application()
