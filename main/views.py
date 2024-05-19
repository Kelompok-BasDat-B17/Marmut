from django.shortcuts import render, redirect
from lib_database.query import *
from lib_database.user import *
from lib_database.playlist import *
import datetime
from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
import uuid

# Create your views here.
def show_main(request):
    return render(request, "main.html")

@csrf_exempt
def user_login(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        data = search_user(email, password)
        if data == "Pengguna":
            response = HttpResponseRedirect(reverse("main:homepage"))
            subscription = check_subscription(email)
            response.set_cookie("email", email)
            response.set_cookie("subscription", subscription)
            return response
        elif data == "Label":
            response = HttpResponseRedirect(reverse("main:homepage"))
            response.set_cookie("email", email)
            return response
        messages.error(request, 'Sorry, incorrect username or password. Please try again.')
    return render(request, "login.html")

def index(request):
    email = request.user.email
    role = get_user_type(email)
    if role == "Label":
        data = get_data_label(email)
        return render(request, "index_label.html", {'id': data[0][0], 'nama': data[0][1], 'email': data[0][2], 'kontak': data[0][4]})
    else:
        return redirect('main:homepage')

def register_option(request):
    return render(request, "register_base.html")

def register_user(request):
    return render(request, "register_pengguna.html")

@csrf_exempt
def register_label(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        nama = request.POST.get("nama")
        kontak = request.POST.get("kontak")
        data = search_label(email, password)
        if len(data) != 0:
            messages.info(request, 'Email already registered')
            return render(request, "register_label.html")
        else:
            uu_id = str(uuid.uuid4())
            id_pemilik_hak_cipta = str(uuid.uuid4())
            insert_label(uu_id, nama, email, password, kontak,id_pemilik_hak_cipta)
            user = User.objects.create_user(email=email, password=password, username=uu_id)
            user.save()
            login(request, user)
            return HttpResponseRedirect(reverse('main:index_label'))
    return render(request, "register_label.html")

def royalty_list(request):
    if not request.user.is_authenticated:
        messages.info(request, 'Please login first')
        return redirect('main:user_login')
    email = request.user.email
    royalty_list = get_royalty_list(email)
    name = get_user_name(email)
    return render(request, "royalty_list.html", {'royalty_list': royalty_list, 'name': name})

@csrf_exempt
def homepage(request):
    if check_user(request.COOKIES.get("email")) == False:
        label = get_label(request.COOKIES.get("email"))
        context = {
            "nama": label[0][1],
            "email": label[0][2],
            "kontak": label[0][4],
            "is_pengguna": False
        }
    else:
        account = get_account(request.COOKIES.get("email"))
        gender = ""
        role = ""
        has_role = get_role(request.COOKIES.get("email"))
        
        if (len(has_role) != 0):
            role += has_role[0]
            for i in range(1, len(has_role)):
                role += ", " + has_role[i]
        else: role = "Tidak mempunyai role"
        print(has_role)
        if account[0][3] == 0:
            gender = "Perempuan"
        else:
            gender = "Laki-laki"

        context = {
            "email": account[0][0],
            "username": account[0][2],
            "gender": gender,
            "tempat_lahir": account[0][4],
            "tanggal_lahir": account[0][5],
            "kota_asal": account[0][7],
            "subscription": request.COOKIES.get("subscription"),
            "role": role,
            "is_pengguna": True
        }
    return render(request, "index.html", context)

def logout(request):
    response = HttpResponseRedirect(reverse('main:show_main'))
    Songs.list_song.clear()
    Playlist.list_playlist.clear()
    response.delete_cookie('email')
    response.delete_cookie('subscription')
    return response

def album_list(request):
    email = request.user.email
    role = get_user_type(email)
    if role == "Label":
        name = get_label_name(email)
    else :  
        name = get_user_name(email)
        
    if role == "Label":
        album_list = get_album_list_label(email)
        return render(request, "album_list_label.html", {'album_list': album_list, 'name': name})
    
    if role == "Artist" or role == "Songwriter":
        album_list = get_album_list_non_label(email)
        if role == "Artist":
            return render(request, "album_list_artist.html", {'album_list': album_list, 'name': name})
        else:
            return render(request, "album_list_songwriter.html", {'album_list': album_list, 'name': name})
    
def album_detail(request, album_id):
    song_list = get_song_list(album_id)
    album_name = get_album_name(album_id)
    return render(request, "album_list_song.html", {'song_list': song_list, 'album_name': album_name})

def delete_album(request, album_id):
    delete_album_by_id(album_id)
    return redirect('main:album_list')

def delete_song(request, song_id):
    album_id = get_album_id_by_song_id(song_id)
    delete_song_by_id(song_id)
    return redirect('main:album_detail', album_id=album_id)

def song_detail(request, song_id):
    song_detail = get_song_detail(song_id)
    album_id = get_album_id_by_song_id(song_id)
    return render(request, "song_detail.html", {'song_detail': song_detail, 'album_id': album_id})
   
def create_album(request):
    if request.method == "POST":
        album_id = str(uuid.uuid4())
        album_name = request.POST.get("album-name")
        album_label = request.POST.get("album-label")
        album_label_id = get_label_uuid_by_name(album_label)
        jumlah_lagu = 0
        total_durasi = 0
        insert_album(album_id, album_name, jumlah_lagu, album_label_id, total_durasi)
        return redirect('main:album_list')
    label_list = get_label_list()
    return render(request, "create_album.html", {'label_list': label_list})

def create_song_songwriter(request, album_id):
    songwriter_name = get_songwriter_name(request.user.username)
    artist_list = get_artist_list()
    album_name = get_album_name(album_id)
    genres = [
    "Pop",
    "Rock",
    "Hip-hop/Rap",
    "Country",
    "Jazz",
    "Blues",
    "Electronic/Dance",
    "R&B (Rhythm and Blues)",
    "Reggae",
    "Folk",
    "Indie",
    "Metal",
    "Punk",
    "Classical",
    "Latin",
    "World",
    "Funk",
    "Gospel",
    "Ambient",
    "Experimental"
]
    if request.method == "POST":
        song_id = str(uuid.uuid4())
        song_name = request.POST.get("song-name")
        song_artist_id = request.POST.get("song-artist")
        song_writer = request.POST.get("song-writer")
        song_genre = request.POST.getlist("song-genre")
        song_duration = request.POST.get("song-duration")
        add_song_songwriter(song_id, song_name, song_artist_id, song_writer, song_genre, song_duration, album_id)
        return redirect('main:album_detail', album_id=album_id)
    return render(request, "create_song_songwriter.html", {'album_name': album_name, 'songwriter_name': songwriter_name, 'artist_list': artist_list, 'genres': genres})

def create_song_artist(request, album_id):
    artist_name = get_artist_name(request.user.username)
    songwriter_list = get_songwriter_list()
    genres = [
    "Pop",
    "Rock",
    "Hip-hop/Rap",
    "Country",
    "Jazz",
    "Blues",
    "Electronic/Dance",
    "R&B (Rhythm and Blues)",
    "Reggae",
    "Folk",
    "Indie",
    "Metal",
    "Punk",
    "Classical",
    "Latin",
    "World",
    "Funk",
    "Gospel",
    "Ambient",
    "Experimental"
]
    if request.method == "POST":
        song_id = str(uuid.uuid4())
        song_name = request.POST.get("song-name")
        song_artist_name = request.POST.get("song-artist")
        song_artist_id = get_artist_id_by_name(song_artist_name)
        song_writers = request.POST.getlist("song-writer")
        song_genres = request.POST.getlist("song-genre")
        song_duration = request.POST.get("song-duration")
        add_song_artist(song_id, song_name, song_artist_id, song_writers, song_genres, song_duration, album_id)
        return redirect('main:album_detail', album_id=album_id)
    return render(request, "create_song_artist.html", {'album_name': album_id, 'artist_name': artist_name, 'genres': genres, 'songwriter_list': songwriter_list})