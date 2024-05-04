from django.shortcuts import render

# Create your views here.
def show_main(request):
    return render(request, "main.html")

def login(request):
    return render(request, "login.html")

def register_option(request):
    return render(request, "register_base.html")

def register_user(request):
    return render(request, "register_pengguna.html")

def register_label(request):
    return render(request, "register_label.html")
