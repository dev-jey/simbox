from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from django_countries.fields import CountryField
from project_box.apps.mods.models import Mod


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=120, blank=True)
    country = CountryField(blank=True)
    bio = models.TextField(max_length=2000, blank=True, null=True)
    twitter = models.CharField(max_length=25, blank=True, help_text='Enter your Twitter username. NOT the link.')
    simulators = models.ManyToManyField(Mod)
    image = models.ImageField(default='default.jpg', upload_to='profile')
    header_image = models.ImageField(default='default.jpg', upload_to='profile/header/')

    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        # img = Image.open(self.image.path)

        # if img.height > 1080 or img.width > 1920:
        #     output_size = (1080, 1920)
        #     img.thumbnail(output_size)
        #     img.save(self.image.path)
