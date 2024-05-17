from django.urls import path
from main.views import *
from melihat_chart.views import melihat_chart, daily_top,weekly_top, monthly_top, yearly_top
from play_podcast.views import play_podcast
from play_song.views import play_song
from play_user_playlist.views import play_user_playlist

app_name = 'main'

urlpatterns = [
    path('', show_main, name='show_main'),
    path('login/', login, name='login'),
    path('register-option/', register_option, name='register_option'),
    path('register-option/register-user/', register_user, name='register_user'),
    path('register-option/register-label/', register_label, name='register_label'),
    path('login/homepage/', homepage, name="homepage"),
    path('logout/', logout, name="logout"),
    path('play-podcast/<uuid:podcast_id>/', play_podcast, name='play_podcast'),
    path('play-song/<uuid:song_id>/', play_song, name='play_song'),
    path('melihat-chart/', melihat_chart, name='melihat_chart'),
    path('melihat-chart/daily-top/', daily_top, name='daily_top'),
    path('melihat-chart/weekly-top/', weekly_top, name='weekly_top'),
    path('melihat-chart/monthly-top/', monthly_top, name='monthly_top'),
    path('melihat-chart/yearly-top/', yearly_top, name='yearly_top'),
        path('play-user-playlist/<uuid:user_playlist_id>/', play_user_playlist, name='play_user_playlist'),
]