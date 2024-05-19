from django.urls import path
from playlist.views import *

app_name = 'playlist'

urlpatterns = [
  path('', show_playlist, name='show_playlist'),
  path('playlist_detail/<str:id_playlist>', playlist_detail, name='playlist_detail'),
  path('add_playlist/', add_playlist, name='add_playlist'),
  path('delete_playlist/<str:id_playlist>', delete_playlist, name="delete_playlist"),
  path('add_song/<str:id_playlist>', add_song, name="add_song"),
  path('playlist_detail/delete_song/<str:id_playlist>/<str:id_song>', delete_song, name="delete_song")
]