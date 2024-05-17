from django.urls import path
from play_user_playlist.views import play_user_playlist

app_name = 'play_podcast'

urlpatterns = [
    path('play-user-playlist/<uuid:user_playlist_id>/', play_user_playlist, name='play_user_playlist'),
]
