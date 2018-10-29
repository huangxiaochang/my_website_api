from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'register/$', views.RegisterView.as_view(), name="user_register"),
    url(r'login/$', views.LoginView.as_view(), name="user_login"),
    url(r'login_out/$', views.login_out.as_view(), name="login_out"),
    url(r'get_user_info/$', views.get_user_info, name="user_info"),
    url(r'modify_user_info', views.modify_user_info, name="modify_user_info"),
    url(r'upload_avatar/$', views.uploadView.as_view(), name="upload_avatar"),
    url(r'export_user_info', views.export_user_info, name="export_user_info"),
    # url(r'captcha_img/', views.create_captcha_img, name="create_captcha_img")
]