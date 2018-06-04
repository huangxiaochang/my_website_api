from django.conf.urls import url, include

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    # url(r'register/', views.RegisterView.as_view(), name="user_register")
    url(r'user_info/', include('api.user_info.urls'))
]