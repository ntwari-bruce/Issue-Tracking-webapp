# Generated by Django 4.2.3 on 2023-07-22 19:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bug_tracker', '0011_notification'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='content',
            field=models.TextField(null=True),
        ),
    ]