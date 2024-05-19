from django.urls import path
from main.views import *

app_name = 'main'

urlpatterns = [
    path('', show_main, name='show_main'),
    path('user_login/', user_login, name='user_login'),
    path('register-option/', register_option, name='register_option'),
    path('register-option/register-user/', register_user, name='register_user'),
    path('register-option/register-label/', register_label, name='register_label'),
    path('index/', index, name='index'),
    path('album_list/', album_list, name='album_list'),
    path('album_detail/<str:album_name>/', album_detail, name='album_detail'),
    path('delete_album/<str:album_name>/', delete_album, name='delete_album'),
    path('song_detail/<str:song_name>/', song_detail, name='song_detail'),
    path('delete_song/<str:song_name>/', delete_song, name='delete_song'),
    path('royalty_list/', royalty_list, name='royalty_list'),
    path('homepage/', homepage, name="homepage"),
    path('logout/', logout, name="logout"),
    path('create_album/', create_album, name='create_album'),
    path('create_song_songwriter/<str:album_name>/', create_song_songwriter, name='create_song_songwriter'),
    path('create_song_artist/<str:album_name>/', create_song_artist, name='create_song_artist'),
    #  path('play-podcast/<uuid:podcast_id>/', play_podcast, name='play_podcast'),
    # path('play-song/<uuid:song_id>/', play_song, name='play_song'),
    # path('melihat-chart/', melihat_chart, name='melihat_chart'),
    # path('melihat-chart/<uuid:chart_id>', chart_detail, name='chart_detail'),
]
