from django.db import models
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator
from django.db.models.fields.related import ForeignKey
# from tinymce.models import HTMLField
from .validators import validate_file_size_10mb, validate_file_size_4mb
from model_utils import FieldTracker


class Simulator(models.Model):
    '''Table with all simulators to allow categorization of mods.'''
    simulator = models.CharField(max_length=100)

    def __str__(self):
        return self.simulator


class ModsType(models.Model):
    '''
    Table with mod types (eg. Scenery, Airplane etc.) for
    categorization of mods.
    '''
    type = models.CharField(max_length=100)

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
        on_delete=models.PROTECT
    )
    simulators = models.ManyToManyField(Simulator)
    type = models.ForeignKey(ModsType, null=True, on_delete=models.SET_NULL)

    tracker = FieldTracker(fields=['mod_file', 'image', 'header_image'])

    def __str__(self):
        return self.title


class ModsLike(models.Model):
    '''Table that stores likes for mods. Each user can like a mod only once.'''
    mod_id = models.ForeignKey(
        Mod,
        null=False,
        default=User,
        on_delete=models.CASCADE
    )
    user_id = models.ForeignKey(
        User,
        null=False,
        default=User,
        on_delete=models.CASCADE
    )
    datetime_liked = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('mod_id', 'user_id')


class ModsView(models.Model):
    '''Table with views for each mod.'''
    mod_id = models.ForeignKey(Mod, null=False, on_delete=models.CASCADE)
    IPAddress = models.GenericIPAddressField(blank=False)
    datetime_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('mod_id', 'IPAddress')


class ModsDownloadsCounter(models.Model):
    mod_id = models.ForeignKey(Mod, null=False, on_delete=models.CASCADE)
    IPAddress = models.GenericIPAddressField(blank=False)
    datetime_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('mod_id', 'IPAddress')


class ModsListName(models.Model):
    '''Model where users can store lists with mods'''
    list_name = models.CharField(max_length=50)
    list_owner = models.ForeignKey(User, default=1, on_delete=models.CASCADE)
    datetime_created = models.DateTimeField(auto_now_add=True)
    datetime_updated = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('list_name', 'list_owner')

    def __str__(self):
        return self.list_name


class ModsListConnector(models.Model):
    '''
    Model that connects mods to lists and vice versa. 
    Users are also connected to lists here.
    '''
    list_id = models.ForeignKey(ModsListName, on_delete=models.CASCADE)
    mod_id = models.ForeignKey(Mod, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    datetime_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('list_id', 'mod_id')


class ModsGallery(models.Model):
    # FIXME: Apply same saving logic as mod for images
    '''Screenshot mod that saves all screenshots for all mods.'''
    mod = models.ForeignKey(Mod, default=None, on_delete=models.CASCADE)
    image = models.ImageField(max_length=250)
    image_thumb = models.ImageField(max_length=250, blank=True)
    datetime_created = models.DateTimeField(auto_now_add=True)
    datetime_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.mod.title


class ModComments(models.Model):
    text = models.TextField(max_length=2000, blank=False)
    user_id = ForeignKey(User, on_delete=models.CASCADE)
    mod_id = ForeignKey(Mod, on_delete=models.CASCADE)
    visible = models.BooleanField(default=True)
    datetime_created = models.DateTimeField(auto_now_add=True)
    datetime_updated = models.DateTimeField(auto_now=True)
