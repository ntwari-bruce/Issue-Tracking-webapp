from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    phone_number = models.CharField(max_length=20)
    
    # Add any other fields you need for your user model

    def __str__(self):
        return self.username

class Project(models.Model):
    project_name = models.CharField(max_length=255)
    project_description = models.TextField()
    team_members = models.ManyToManyField(CustomUser)

    def __str__(self):
        return self.project_name