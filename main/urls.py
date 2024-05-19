from django.urls import path
from main.views import *
from melihat_chart.views import melihat_chart, daily_top,weekly_top, monthly_top, yearly_top
from play_podcast.views import play_podcast
from play_song.views import play_song
from play_user_playlist.views import play_user_playlist

app_name = 'main'

urlpatterns = [
    path('', show_main, name='show_main'),
    path('user_login/', user_login, name='user_login'),
    path('register-option/', register_option, name='register_option'),
    path('register-option/register-user/', register_user, name='register_user'),
    path('register-option/register-label/', register_label, name='register_label'),
    path('homepage/', homepage, name="homepage"),
    path('logout/', logout, name="logout"),
    path('play-podcast/<uuid:podcast_id>/', play_podcast, name='play_podcast'),
    path('play-song/<uuid:song_id>/', play_song, name='play_song'),
    path('melihat-chart/', melihat_chart, name='melihat_chart'),
    path('melihat-chart/daily-top/', daily_top, name='daily_top'),
    path('melihat-chart/weekly-top/', weekly_top, name='weekly_top'),
    path('melihat-chart/monthly-top/', monthly_top, name='monthly_top'),
    path('melihat-chart/yearly-top/', yearly_top, name='yearly_top'),
    path('play-user-playlist/<uuid:user_playlist_id>/', play_user_playlist, name='play_user_playlist'),
    path('index/', index, name='index'),
    path('album_list/', album_list, name='album_list'),
    path('album_detail/<str:album_name>/', album_detail, name='album_detail'),
    path('delete_album/<str:album_name>/', delete_album, name='delete_album'),
    path('song_detail/<str:song_name>/', song_detail, name='song_detail'),
    path('delete_song/<str:song_name>/', delete_song, name='delete_song'),
    path('royalty_list/', royalty_list, name='royalty_list'),  
    path('create_album/', create_album, name='create_album'),
    path('create_song_songwriter/<str:album_name>/', create_song_songwriter, name='create_song_songwriter'),
    path('create_song_artist/<str:album_name>/', create_song_artist, name='create_song_artist'),
]
