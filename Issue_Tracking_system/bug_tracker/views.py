from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, request, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from .models import CustomUser, Project, Ticket, Comment
from django.contrib import auth
from django.contrib.auth import authenticate,login as auth_login, logout as auth_logout, get_backends
from django.urls import reverse
from .backends import CustomUserBackend
from django.http import JsonResponse,HttpResponseServerError
from django.core.paginator import Paginator
import json
from django.core.serializers.json import DjangoJSONEncoder
from django.core.serializers import serialize


# Create your views here
def index(request):
    if request.method == 'GET':
        # Get all users in the system
        users = CustomUser.objects.all()

        # Get all projects
        projects = Project.objects.all().order_by("id")

        # Pagination
        paginator = Paginator(projects, 5)  # Display 5 projects per page
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        return render(request, "bug_tracker/index.html", {
            "users": users,
            "projects": projects,
            "project_list": page_obj,
            "page_range": paginator.page_range,
            "page_number": page_obj.number,
        })

# Registering for the user account
def register(request):
    if request.method == "POST":
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
        user = CustomUser.objects.create_user(first_name=first_name, username=first_name, last_name=last_name,phone_number=phone_number, email=email, password=password)
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

#deleting a project
def delete_project(request, id):
    if request.method == "DELETE":
        # Handle any error that might happen
        try:
            project = Project.objects.get(id=id)
            project.delete()
            return JsonResponse({"message": "Project deleted successfully"})
        except Project.DoesNotExist:
            return JsonResponse({"error": "Project not found"}, status=404)
        except Exception as e:
            return HttpResponseServerError(str(e))
        return HttpResponseRedirect(reverse("index"))

# Project full details
def project_view(request, id):
    if request.method == "GET":
        users = CustomUser.objects.all()
        project = Project.objects.get(id=id)
        team_members = project.team_members.all().order_by("id")
        # querying for all the tickets
        tickets = project.project_tickets.all().order_by("id")
        # pagination for tickets
        paginator1 = Paginator(tickets, 4)
        page_number1 = request.GET.get('page1')
        page_obj1 = paginator1.get_page(page_number1)
        # Pagination
        paginator = Paginator(team_members, 3)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, "bug_tracker/project.html", {
            "team_members": page_obj,
            "project": project,
            "page_range": paginator.page_range,
            "page_number": page_obj.number,
            "users": users,
            "page_range1": paginator1.page_range,
            "page_number1": page_obj1.number,
            "tickets": page_obj1
        })

# updating members
def update_members(request, id):
    project = Project.objects.get(id=id)

    if request.method == "POST":
        # Getting all the team members ids
        team_members_ids = request.POST.getlist("sellist2b")
        # Getting the team members
        team_members = CustomUser.objects.filter(pk__in=team_members_ids)
        project.team_members.set(team_members)
        return HttpResponseRedirect(reverse("project_view", kwargs={"id": id}))

# deleting a team_member from the project
def delete_member(request, project_id, member_id):
    if request.method == "DELETE":
        project = get_object_or_404(Project, id=project_id)
        team_member = get_object_or_404(CustomUser, id=member_id)
        project.team_members.remove(team_member)
        # Return an empty response with status code 204 (No Content)
        return HttpResponse(status=204)  

# creating a tciket
def create_ticket(request, project_id):
    if request.method == "POST":
        title = request.POST.get("title")
        description = request.POST.get("description")
        team_members_ids = request.POST.getlist("sellist2c")
        time_estimate = request.POST.get("time")
        ticket_type = request.POST.get("typec")
        priority = request.POST.get("priorityc")
        status = request.POST.get("status")

        # Get the project instance
        project = Project.objects.get(id=project_id)
        

        # Create the ticket
        ticket = Ticket.objects.create(
            project=project,
            title=title,
            description=description,
            author=request.user, 
            status=status,
            priority=priority,
            ticket_type=ticket_type,
            estimated_time=time_estimate
        )
        # assigned devs
        team_members = CustomUser.objects.filter(pk__in=team_members_ids)
        ticket.assigned_devs.set(team_members)

        # Redirect to the project details page
        return HttpResponseRedirect(reverse("project_view", kwargs={"id": project_id}))


# delete a ticket
def delete_ticket(request, project_id, ticket_id):
    if request.method == "DELETE":
        project = get_object_or_404(Project, id=project_id)
        ticket = get_object_or_404(Ticket, id=ticket_id)
        project.project_tickets.remove(ticket)
        return HttpResponse(status=204)
    else:
        return HttpResponse(status=405) 

# editing the ticket
def edit_ticket(request, project_id, ticket_id):
    try:
        project = Project.objects.get(id=project_id)
        ticket = project.project_tickets.get(id=ticket_id)
        data = {
            'ticket':{
                        'title': ticket.title,
                        'description': ticket.description,
                        'author': {
                                'id': ticket.author.id,
                                'first_name': ticket.author.first_name,
                                'last_name': ticket.author.last_name
                            },
                        'status': ticket.status,
                        'priority': ticket.priority,
                        'ticket_type': ticket.ticket_type,
                        'estimated_time': ticket.estimated_time,
                        'assigned_devs': list(ticket.assigned_devs.values('id', 'first_name', 'last_name')),
            }
            
            
        }
        return JsonResponse(data, safe=False)
    except Project.DoesNotExist:
        return JsonResponse({'error': 'ticket not found'}, status=404)

# update the edited ticket   
def update_ticket(request, project_id):
    project = Project.objects.get(id=project_id)  
    if request.method == "POST":
        title = request.POST.get('Title')  
        ticket_id = request.POST.get('ticket_id')
        description = request.POST.get('title_description')  
        assigned_devs = request.POST.getlist('ticket-sel')  
        time_estimate = request.POST.get('Time')  
        priority = request.POST.get('priority')  
        status = request.POST.get('status') 
        print("This is the ticket id:", ticket_id)
        # Update the ticket object with the new values
        ticket = Ticket.objects.get(id=ticket_id)
        ticket.title = title
        ticket.description = description
        ticket.assigned_devs.set(assigned_devs)  
        ticket.time_estimate = time_estimate
        ticket.priority = priority
        ticket.status = status
        ticket.save()

        return HttpResponseRedirect(reverse("project_view", kwargs={"id": project_id}))

# getting the details for the ticket
def get_ticket_details(request, project_id, ticket_id):
    ticket = Ticket.objects.get(id=ticket_id)
    assigned_devs = ticket.assigned_devs.all()
    comments = ticket.comments.all()

    comments_list = []
    for comment in comments:
        comment_dict = {
            'id': comment.id,
            'author': {
                'first_name': comment.author.first_name,
                'last_name': comment.author.last_name,
            },
            'content': comment.content,
            'created_at': comment.created_at,
        }
        comments_list.append(comment_dict)

    data = {
        'title': ticket.title,
        'author': ticket.author.username,
        'description': ticket.description,
        'status': ticket.status,
        'priority': ticket.priority,
        'ticket_type': ticket.ticket_type,
        'estimated_time': ticket.estimated_time,
        'assigned_devs': [f"{dev.first_name} {dev.last_name}" for dev in assigned_devs],
        'comments': comments_list,
    }

    return JsonResponse(data)


# saving the comment
def save_comment(request):
    if request.method == 'POST':
        ticket_id = request.POST.get('ticketId')
        project_id = request.POST.get('projectId')
        content = request.POST.get('content')

        # Create a new comment object
        comment = Comment.objects.create(
            ticket_id=ticket_id,
            author=request.user,
            content=content
        )

        # Prepare the data to be sent back as the JSON response
        response_data = {
            'id': comment.id,
            'author': {
                'first_name': comment.author.first_name,
                'last_name': comment.author.last_name
            },
            'created_at': comment.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'content': comment.content
        }
        print("These are the response data:",response_data)
        return JsonResponse(response_data)

# delete comment
def delete_comment(request, comment_id):
    if request.method == "POST":
        comment = get_object_or_404(Comment, id=comment_id)
        comment.delete()
        return HttpResponse(status=204)
    else:
        return HttpResponse(status=405)