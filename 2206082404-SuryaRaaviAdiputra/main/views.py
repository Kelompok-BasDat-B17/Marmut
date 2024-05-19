from django.shortcuts import render, redirect
from lib_database.query import *
from lib_database.user import *
from lib_database.playlist import *
import datetime
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt


# Create your views here.
def show_main(request):
    return render(request, "main.html")

@csrf_exempt
def login(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        data = search_user(email, password)
        if len(data) != 0:
            val_email = data[0][0]
            response = HttpResponseRedirect(reverse("main:homepage"))
            subscription = check_subscription(val_email)
            response.set_cookie("email", val_email)
            response.set_cookie("subscription", subscription)
           
            return response
        messages.error(request, 'Sorry, incorrect username or password. Please try again.')
    return render(request, "login.html")

def register_option(request):
    return render(request, "register_base.html")

def register_user(request):
    return render(request, "register_pengguna.html")

def register_label(request):
    return render(request, "register_label.html")

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
