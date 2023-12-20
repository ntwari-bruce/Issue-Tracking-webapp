from django.contrib.auth.models import AbstractUser,Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils import timezone
from django.contrib import admin


class CustomUser(AbstractUser):
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    phone_number = models.CharField(max_length=20,blank=False, null=False)
    
    # Add any other fields you need for your user model

    def __str__(self):
        return self.username

class Project(models.Model):
    project_name = models.CharField(max_length=255)
    project_description = models.TextField()
    team_members = models.ManyToManyField(CustomUser)
    project_creator = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='created_projects', null=True)

    def __str__(self):
        return self.project_name

class Ticket(models.Model):
    STATUS_CHOICES = [
        ('New', 'New'),
        ('In Progress', 'In Progress'),
        ('Completed', 'Completed'),
    ]

    PRIORITY_CHOICES = [
        ('Low', 'Low'),
        ('Medium', 'Medium'),
        ('High', 'High'),
    ]

    TYPE_CHOICES = [
        ('Bug', 'Bug'),
        ('Feature', 'Feature'),
        ('Task', 'Task'),
    ]

    project = models.ForeignKey('Project', on_delete=models.CASCADE, related_name='project_tickets', null=True)
    title = models.CharField(max_length=255)
    description = models.TextField()
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES)
    ticket_type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    estimated_time = models.IntegerField()
    assigned_devs = models.ManyToManyField(CustomUser, related_name='assigned_tickets', blank=True)


    def __str__(self):
        return self.title

class Comment(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name='comments', null=True)
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)
    content = models.TextField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.author.username} on {self.ticket.title}"


class Notification(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)
    project = models.ForeignKey('Project', on_delete=models.CASCADE, null=True)
    message = models.CharField(max_length=255)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.user.username} - {self.message}"

class PasswordResetToken(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)
    token = models.CharField(max_length=1000)
    expiration_time = models.DateTimeField()

    def is_expired(self):
        return self.expiration_time < timezone.now()