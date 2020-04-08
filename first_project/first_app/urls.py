from first_app import views
from django.conf.urls import url
from django.urls import re_path,path

app_name='first_app'

urlpatterns=[
    re_path(r'^$',views.index,name='index'),
    path('ish/',views.help,name='help1'),
    path('reg/',views.reg,name='reg2'),
    path('rel/',views.rel,name='rel3'),
    path('register/',views.register,name='register'),
    path('login/',views.user_login,name='user_login'),
]
