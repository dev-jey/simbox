# Generated by Django 3.1.6 on 2021-05-02 11:49

from django.db import migrations, models
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0002_auto_20210417_1242'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=120)),
                ('email', models.CharField(max_length=120)),
                ('description', tinymce.models.HTMLField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]