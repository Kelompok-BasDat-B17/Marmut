from django.shortcuts import render, redirect
from lib_database.query import *
from lib_database.user import *
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
        print(data)
        if len(data) != 0:
            val_email = data[0][0]
            response = HttpResponseRedirect(reverse("main:homepage"))
            subscription = check_subscription(val_email)
            response.set_cookie("email", val_email)
            response.set_cookie("subscription", subscription)
            print(subscription)
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
    account = get_account(request.COOKIES.get("email"))
    gender = ""
    print(account)
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
        "subscription": request.COOKIES.get("subscription")
    }
    return render(request, "index.html", context)

def logout(request):
    response = HttpResponseRedirect(reverse('main:show_main'))

    response.delete_cookie('email')
    response.delete_cookie('subscription')
    
    return response
