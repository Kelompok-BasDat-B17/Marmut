from django.shortcuts import render, redirect
from lib_database.query import *
from lib_database.playlist import *
import datetime
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import uuid

def show_playlist(request):
  playlist = get_playlist(request.COOKIES.get("email"))
  print(playlist)
  if (len(playlist) != 0):
    print(playlist)
    pembuat = get_pembuat(request.COOKIES.get("email"))
    print(pembuat)
    Playlist.list_playlist.clear()
    for i in range(len(playlist)):
      if playlist[i][4] == None:
        Playlist(playlist[i][0], playlist[i][1], playlist[i][2], playlist[i][3], 0, playlist[i][5])
      else:
        Playlist(playlist[i][0], playlist[i][1], playlist[i][2], playlist[i][3], playlist[i][4], playlist[i][5])
    context = {
      "has_playlist": True, 
      "list_playlist": Playlist.list_playlist
    }
    return render(request, "playlist.html", context)
  return render(request, "playlist.html", context={"has_playlist": False})

def playlist_detail(request, id_playlist):
  user_detail = get_user_detail(id_playlist)
  list_song = get_detail_playlist(id_playlist)
  print(user_detail.id_playlist)
  print(id_playlist)
  print(list_song)
  Songs.list_song.clear()
  if len(list_song) != 0:
    for song in list_song:
      Songs(song[0], song[1], song[2], song[3])
    context = {
      "songs": Songs.list_song,
      "user_detail": user_detail,
      "pembuat": get_pembuat(request.COOKIES.get("email"))[0][0]
    }
    return render(request, "user_playlist_detail.html", context)
  return render(request, "user_playlist_detail.html", context={"user_detail": user_detail, "pembuat": get_pembuat(request.COOKIES.get("email"))[0][0]})

@csrf_exempt
def add_playlist(request):
  if request.method == "POST":
      email = request.COOKIES.get("email")
      judul = request.POST.get("judul")
      deskripsi = request.POST.get('deskripsi')
      id_user_playlist = uuid.uuid1()
      id_playlist = uuid.uuid1()
      insert_playlist(id_playlist, judul, deskripsi, email, id_user_playlist)
      return HttpResponseRedirect(reverse('playlist:show_playlist'))
  return render(request, "add_playlist.html")

def delete_playlist(request, id_playlist):
  del_playlist(id_playlist)
  return HttpResponseRedirect(reverse('playlist:show_playlist'))

def add_song(request, id_playlist):
  get_song = get_list_lagu()
  Songs.list_song.clear()
  for song in get_song:
    Songs(song[1], song[2], 0, song[0])
  context = {
    "list_song": Songs.list_song
  }
  return render(request, "add_song.html", context)


   
# Create your views here.
