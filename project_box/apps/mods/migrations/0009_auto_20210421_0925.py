# Generated by Django 3.1.6 on 2021-04-21 09:25

import django.core.validators
from django.db import migrations, models
import project_box.apps.mods.validators


class Migration(migrations.Migration):

    dependencies = [
        ('mods', '0008_auto_20210420_1335'),
    ]

    operations = [
        migrations.CreateModel(
            name='Screenshot',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.FileField(help_text='You can upload up to 12 screenshots. Max file size: 4MB', upload_to='', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['png', 'jpg']), project_box.apps.mods.validators.validate_file_size_4mb])),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.RenameField(
            model_name='mod',
            old_name='image',
            new_name='header_image',
        ),
        migrations.AddField(
            model_name='mod',
            name='screenshots',
            field=models.ManyToManyField(blank=True, related_name='user_comments', to='mods.Screenshot'),
        ),
    ]