from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, request, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from .models import CustomUser, Project
from django.contrib import auth
from django.contrib.auth import authenticate,login as auth_login, logout as auth_logout, get_backends
from django.urls import reverse
from .backends import CustomUserBackend
from django.http import JsonResponse

# Create your views here
def index(request):
    if request.method == 'GET':
        # Get all users in the system
        users = CustomUser.objects.all()
        # Get all projects
        projects = Project.objects.all()
        return render(request, "bug_tracker/index.html",{
            "users": users,
            "projects": projects
        })

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
            "message": "Account already exists!"
        })
        user = CustomUser.objects.create_user(first_name=first_name, username=first_name, last_name=last_name, email=email, password=password)
        user.backend = f"{get_backends()[0].__module__}.{get_backends()[0].__class__.__name__}"
        user.save()
        auth_login(request, user, backend=user.backend)
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
    if request.method == "POST":
        auth_logout(request)
        return render(request,"bug_tracker/layout.html")

# getting back to layout
def layout(request):
    return render(request, "bug_tracker/layout.html",)

# Creating a new project
def create_project(request):
    if request.method == "POST":
        project_name = request.POST.get("project_name")
        project_description = request.POST.get("project_description")
        team_members_ids = request.POST.getlist("sellist2a")
        project = Project(project_name=project_name, project_description=project_description, project_creator=request.user)
        project.save()
        team_members = CustomUser.objects.filter(pk__in=team_members_ids)
        project.team_members.set(team_members)
        return HttpResponseRedirect(reverse("index"))
        

# Retrieving project details for editing project
def project_detail(request, pk):
    try:
        project = Project.objects.get(pk=pk)
        data = {
            'project_name': project.project_name,
            'project_description': project.project_description,
            'team_members': list(project.team_members.values_list('id', flat=True)),
        }
        return JsonResponse({'project': data})
    except Project.DoesNotExist:
        return JsonResponse({'error': 'Project not found'}, status=404)
# Updating the edited project
def update_project(request):
    if request.method == "POST":
        project_id = request.POST.get("project_id")
        project_name = request.POST.get("project_name")
        project_description = request.POST.get("project_description")
        team_members_ids = request.POST.getlist("sellist2a")

        # Update in the database
        project = Project.objects.get(id=project_id)
        project.project_name = project_name
        project.project_description = project_description
        project.save()
        team_members = CustomUser.objects.filter(pk__in=team_members_ids)
        project.team_members.set(team_members)
        return HttpResponseRedirect(reverse("index"))