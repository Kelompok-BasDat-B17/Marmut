from django.urls import path
from play_song.views import add_song_to_playlist, play_song, update_play_count

app_name = 'play_song'

urlpatterns = [
    path('play-song/<uuid:song_id>/', play_song, name='play_song'),
    path('update-play-count/<uuid:song_id>/', update_play_count, name='update-play-count'),
    path('play-song/<uuid:song_id>/add-song-to-playlist/', add_song_to_playlist, name='add_song_to_playlist'),
]
