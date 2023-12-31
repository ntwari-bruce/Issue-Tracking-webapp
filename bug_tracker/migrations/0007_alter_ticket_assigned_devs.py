# Generated by Django 4.2.3 on 2023-07-11 01:58

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bug_tracker', '0006_ticket_assigned_devs'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticket',
            name='assigned_devs',
            field=models.ManyToManyField(null=True, related_name='assigned_tickets', to=settings.AUTH_USER_MODEL),
        ),
    ]
