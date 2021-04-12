from django.db import models
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator
from django.db.models.fields.related import ForeignKey
# from tinymce.models import HTMLField
from .validators import validate_file_size_10mb, validate_file_size_4mb
from model_utils import FieldTracker


class ModsType(models.Model):
    '''
    Table with mod types (eg. Scenery, Airplane etc.) for
    categorization of mods.
    '''
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.type


class Mod(models.Model):
    title = models.CharField(max_length=120)
    image = models.ImageField(
        blank=False,
        validators=[FileExtensionValidator(allowed_extensions=['png']), validate_file_size_4mb],
        help_text="Allowed format: PNG. Max. size: 4MB"
    )
    header_image = models.ImageField(
        blank=False,
        validators=[FileExtensionValidator(allowed_extensions=['png']), validate_file_size_4mb],
        help_text="Allowed format: PNG. Max. size: 4MB"
    )
    description = models.TextField(max_length=10000)

    mod_file = models.FileField(
        blank=False,
        validators=[FileExtensionValidator(allowed_extensions=['zip']), validate_file_size_10mb],
        help_text="Please upload a .zip file. Current max. size: 10Mb."
    )
    mod_file_size = models.FloatField(blank=True)

    datetime_created = models.DateTimeField(auto_now_add=True)
    datetime_updated = models.DateTimeField(auto_now=True)
    visible = models.BooleanField(default=False)
    verified = models.BooleanField(default=False)

    # Relationships
    author = models.ForeignKey(
        User,
        null=True,
        default=User,
        on_delete=models.PROTECT)
    type = models.ForeignKey(ModsType, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.title


class ModsDownloadsCounter(models.Model):
    mod_id = models.ForeignKey(Mod, null=False, on_delete=models.CASCADE)
    IPAddress = models.GenericIPAddressField(blank=False)
    datetime_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('mod_id', 'IPAddress')


class ModComments(models.Model):
    text = models.TextField(max_length=2000, blank=False)
    user_id = ForeignKey(User, on_delete=models.CASCADE)
    mod_id = ForeignKey(Mod, on_delete=models.CASCADE)
    visible = models.BooleanField(default=True)
    datetime_created = models.DateTimeField(auto_now_add=True)
    datetime_updated = models.DateTimeField(auto_now=True)
