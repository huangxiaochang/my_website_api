"""my_website_api URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include

from api.views import page_not_found

from my_website_api import settings

# url(reg, view, kwargs, name)
urlpatterns = [
    url(r'admin/', admin.site.urls),
    url(r'^', include("api.urls")),
    url(r'^login/', include("login.urls")),
    url(r'^captcha', include('captcha.urls')),
    url(r'^device_statistic_index/(.*)$', page_not_found)  # 支持前端vue的history模式，前端的路由要有一个base_router为device_statistic_index
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  # 支持媒体文件路径

# 关于django文件在前端显示的问题：
# 要在目录级的urlpatterns上加上static的路径，这样在前端寻找资源的时候，才能正确找到相应的资源，
# static的第二个参数即为文件存储在项目本地的路径， 第一个参数为前端资源路径的前缀
# 例如在MEDIA_ROOT目录下有资源hxc_123.png,  那么前端显示的资源的相对url为 MEDIA_URL + hxc_123.png
