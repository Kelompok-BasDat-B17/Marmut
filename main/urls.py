from django.urls import path
from main.views import *
from melihat_chart.views import chart_detail, melihat_chart
from play_podcast.views import play_podcast
from play_song.views import play_song

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
    path('melihat-chart/<uuid:chart_id>', chart_detail, name='chart_detail'),
]