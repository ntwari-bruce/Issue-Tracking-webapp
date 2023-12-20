# Generated by Django 4.2.3 on 2023-07-10 16:06

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bug_tracker', '0003_project_project_creator'),
    ]

    operations = [
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('status', models.CharField(choices=[('New', 'New'), ('In Progress', 'In Progress'), ('Completed', 'Completed')], max_length=20)),
                ('priority', models.CharField(choices=[('Low', 'Low'), ('Medium', 'Medium'), ('High', 'High')], max_length=20)),
                ('ticket_type', models.CharField(choices=[('Bug', 'Bug'), ('Feature', 'Feature'), ('Task', 'Task')], max_length=20)),
                ('estimated_time', models.IntegerField()),
                ('author', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('project', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='tickets', to='bug_tracker.project')),
            ],
        ),
    ]