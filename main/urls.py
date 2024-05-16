from django.urls import path
from main.views import *

app_name = 'main'

urlpatterns = [
    path('', show_main, name='show_main'),
    path('user_login/', user_login, name='user_login'),
    path('register-option/', register_option, name='register_option'),
    path('register-option/register-user/', register_user, name='register_user'),
    path('register-option/register-label/', register_label, name='register_label'),
    path('album_list/', album_list, name='album_list'),
    path('royalty_list/', royalty_list, name='royalty_list'),
    path('logout/', logout_user, name='logout_user'),
]
