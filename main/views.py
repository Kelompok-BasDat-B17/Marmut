from django.shortcuts import render, redirect
from lib_database.query import *
from lib_database.user import *
import datetime
from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
# Create your views here.
def show_main(request):
    return render(request, "main.html")

@csrf_exempt
def user_login(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        data = search_user(email, password)

        if len(data) != 0:
            user = authenticate(username=email,email=email, password=password)
            if user is not None:
                login(request, user)
            else : 
                user = User.objects.create_user(email=email, password=password, username=email)
                user.save()
                login(request, user)
            return HttpResponseRedirect(reverse('main:album_list'))
        
        else :
            data = search_label(email, password)
            if len(data) != 0:
                user = authenticate(username=email,email=email, password=password)
                if user is not None:
                    login(request, user)
                else : 
                    user = User.objects.create_user(email=email, password=password, username=email)
                    user.save()
                    login(request, user)
                return HttpResponseRedirect(reverse('main:album_list'))
            else:
                messages.info(request, 'Email or password is incorrect')
                return render(request, "login.html")
                
    return render(request, "login.html")

def register_option(request):
    return render(request, "register_base.html")

def register_user(request):
    return render(request, "register_pengguna.html")

def register_label(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        nama = request.POST.get("nama")
        kontak = request.POST.get("kontak")
        data = search_label(email, password, nama, kontak)
        if len(data) != 0:
            messages.info(request, 'Email already registered')
            return render(request, "register_label.html")
        else:
            insert_label(email, password, nama, kontak)
            user = User.objects.create_user(email=email, password=password, username=email)
            user.save()
            login(request, user)
            return HttpResponseRedirect(reverse('main:album_list'))
    return render(request, "register_label.html")

def royalty_list(request):
    if not request.user.is_authenticated:
        messages.info(request, 'Please login first')
        return redirect('main:user_login')
    email = request.user.email
    royalty_list = get_royalty_list(email)
    name = get_user_name(email)
    return render(request, "royalty_list.html", {'royalty_list': royalty_list, 'name': name})

def logout_user(request):
    logout(request)
    return redirect('main:user_login')
    

def album_list(request):
    email = request.user.email
    role = get_user_type(email)
    if role == "Label":
        name = get_label_name(email)
    else :
        name = get_user_name(email)
    
    if role == "Label":
        return render(request, "album_list_label.html", {'name': name})
    if role == "Artist":
        return render(request, "album_list_artist.html", {'name': name})
    if role == "Songwriter":
        return render(request, "album_list_songwriter.html", {'name': name})

def album_list_song(request):
    email = request.user.email
    role = get_user_type(email)
    if role == "Label":
        name = get_label_name(email)
    else :
        name = get_user_name(email)
    if role == "Label":
        return render(request, "album_list_song_label.html", {'name': name})
    if role == "Artist":
        return render(request, "album_list_song_artist.html", {'name': name})
    if role == "Songwriter":
        return render(request, "album_list_song_songwriter.html", {'name': name})
