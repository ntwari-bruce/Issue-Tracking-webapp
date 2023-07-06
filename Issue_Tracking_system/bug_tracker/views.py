from django.shortcuts import render
from django.http import HttpResponse, request, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from .models import CustomUser
from django.contrib import auth
from django.contrib.auth import authenticate,login as auth_login, logout as auth_logout
from django.urls import reverse
from .backends import CustomUserBackend

# Create your views here
def index(request):
    if request.method == 'GET':
        return render(request, "bug_tracker/index.html")

# Registering for the user account
def register(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        phone_number = request.POST['phone_number']
        email = request.POST['email']
        password = request.POST['password']
        password_confirm = request.POST['password_confirm']

        # check if all fields are completed
        if not(first_name and last_name and phone_number and email and password and password_confirm):
            return render(request, "bug_tracker/register.html", {
                "message": "All fields are required"
            })
        # check if passwords match
        if password != password_confirm:
            return render(request, "bug_tracker/register.html", {
                "message": "Passwords must match."
            })
        
        
        if CustomUser.objects.filter(email=email).exists():
            return render(request, "bug_tracker/register.html", {
            "message": "Account already exists"
        })
        user = CustomUser.objects.create_user(first_name=first_name, username=first_name, last_name=last_name, email=email, password=password)
        user.save()
        auth_login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, 'bug_tracker/register.html')

def login_view(request):
    if request.method == "POST":
        # Attempt to sign user in
        email = request.POST["email"]
        print(email)
        password = request.POST["password"]
        print(password)
        user = authenticate(email=email,password=password)
        print(user)
        # Check if authentication successful
        if user is not None:
            auth_login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "bug_tracker/layout.html", {
                "message": "Invalid email and/or password."
            })
    else:
        return render(request, "bug_tracker/layout.html")

# logout the user
def logout(request):
    if request.method == 'POST':
        auth_logout(request)
        return render(request,"bug_tracker/layout.html")

# getting back to layout
def layout(request):
    return render(request, 'bug_tracker/layout.html',)
