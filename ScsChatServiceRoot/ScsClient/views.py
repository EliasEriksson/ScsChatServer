from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect


def home(request: HttpRequest):
    if request.user.is_authenticated:
        return render(request, "ScsClient/client.html", context={
            "session_key": request.session.session_key
        })
    return redirect("user-login")
