# Generated by Django 3.1.4 on 2021-01-25 15:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='vatsim',
        ),
    ]
