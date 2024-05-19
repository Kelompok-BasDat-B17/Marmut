from django.urls import path
from play_song.views import play_song, update_play_count

app_name = 'play_song'

urlpatterns = [
    path('play-song/<uuid:song_id>/', play_song, name='play_song'),
    path('update-play-count/<uuid:song_id>/', update_play_count, name='update-play-count'),
]
