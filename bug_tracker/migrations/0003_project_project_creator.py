# Generated by Django 4.2.3 on 2023-07-06 19:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bug_tracker', '0002_project'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='project_creator',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='created_projects', to=settings.AUTH_USER_MODEL),
        ),
    ]
