from django.db import models
from django.urls.base import reverse
from django.core.validators import FileExtensionValidator
# from tinymce.models import HTMLField
from .validators import validate_file_size_10mb, validate_file_size_4mb


class Download(models.Model):
    ip_address = models.GenericIPAddressField(protocol='IPv4', default='', unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Comment(models.Model):
    text = models.TextField(max_length=2000, blank=False)
    visible = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Mod(models.Model):
    title = models.CharField(max_length=120)
    image = models.ImageField(
        blank=False,
        validators=[FileExtensionValidator(allowed_extensions=['png', 'jpg', 'jpeg']), validate_file_size_4mb],
        help_text="Max. size: 4MB"
    )
    cover_image = models.ImageField(
        blank=False,
        validators=[FileExtensionValidator(allowed_extensions=['png', 'jpg']), validate_file_size_4mb],
        help_text="Max. size: 4MB"
    )
    description = models.CharField(max_length=10000)
    mod_file = models.FileField(
        blank=False,
        validators=[FileExtensionValidator(allowed_extensions=['zip']), validate_file_size_10mb],
        help_text="Please upload a .zip file. Current max. size: 10Mb."
    )
    uploading_to_cloud = models.BooleanField(default=False, blank=True, null=True)
    downloads = models.ManyToManyField(Download, related_name='mod_downloads', blank=True)
    comments = models.ManyToManyField(Comment, related_name='user_comments', blank=True)
    visible = models.BooleanField(default=False, blank=True, null=True)
    verified = models.BooleanField(default=False, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_absolute_url(self):
        return reverse('mods:mod-detail', args=[self.id])

    def __str__(self):
        return self.title


class Type(models.Model):
    '''
    Table with mod types (eg. Scenery, Airplane etc.) for
    categorization of mods.
    '''
    name = models.CharField(max_length=100)
    mods = models.ManyToManyField(Mod, related_name='type_mods')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
