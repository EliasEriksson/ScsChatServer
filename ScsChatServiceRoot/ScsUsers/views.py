from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpRequest
from .forms import UserRegisterForm


def user_home(request: HttpRequest):
    return render(request, "ScsUsers/home.html")


def user_login(request: HttpRequest):
    if request.method == "POST":
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                return redirect("client-home")
    context = {
        "form": AuthenticationForm()
    }
    return render(request, "ScsUsers/login.html", context=context)


def user_register(request: HttpRequest):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password1"]
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                return redirect("client-home")
    context = {
        "form": UserRegisterForm()
    }
    return render(request, "ScsUsers/register.html", context=context)


def user_logout(request: HttpRequest):
    logout(request)
    return redirect("user-home")
