from django.shortcuts import render
from django.http import HttpResponse, request
from django.contrib.auth.decorators import login_required



# Create your views here
def index(request):
    return render(request, "bug_tracker/index.html")

# Registering for the user account
def register(request):
    if request.method == 'GET':
        return render(request, 'bug_tracker/register.html',)
        
# getting back to layout
def layout(request):
    return render(request, 'bug_tracker/layout.html',)
