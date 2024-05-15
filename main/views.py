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
        if len(data) != 0:
            val_email = data[0][0]
            response = HttpResponseRedirect(reverse("main: homepage "))
            subscription = check_subscription(val_email)
            response.set_cookie("email", val_email)
            response.set_cookie("subscription", subscription)
            return response
        messages.info(request, 'Sorry, incorrect username or password. Please try again.')
    return render(request, "login.html")

def register_option(request):
    return render(request, "register_base.html")

def register_user(request):
    return render(request, "register_pengguna.html")

def register_label(request):
    return render(request, "register_label.html")
