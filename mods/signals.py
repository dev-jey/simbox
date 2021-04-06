from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.conf import settings
from django.template.defaultfilters import slugify
from django.db.models.query import QuerySet

from .models import Mod, ModsGallery

from random import randint
import shutil
import os
import random
from PIL import Image, ImageOps


@receiver(post_save, sender=Mod)
def mod_file_handler(sender, instance, created, **kwargs):

    # Create paths
    mod_folder = os.path.join(settings.MEDIA_ROOT, 'mods', str(instance.id))
    mod_file_folder = os.path.join(mod_folder, "files")

    if created:
        if not os.path.isdir(mod_folder):
            os.mkdir(mod_folder)
            os.mkdir(mod_file_folder)

    # Thumbnail
    if instance.tracker.has_changed('image') or created:
        os.replace(instance.image.path, os.path.join(mod_folder, "thumbnail.png"))
        instance.image = os.path.join(mod_folder, "thumbnail.png")
        img = Image.open(instance.image.path)
        img = ImageOps.fit(img, (200, 200))
        img.save(instance.image.path)
        instance.image = f"mods/{str(instance.id)}/thumbnail.png"

        QuerySet(instance).filter(pk=instance.pk).update(
            image=instance.image
        )

    # Header image
    if instance.tracker.has_changed('header_image') or created:
        os.replace(instance.header_image.path, os.path.join(mod_folder, "header.png"))
        instance.header_image = f"mods/{str(instance.id)}/header.png"

        QuerySet(instance).filter(pk=instance.pk).update(
            header_image=instance.header_image
        )

    if instance.tracker.has_changed('mod_file') and not created:
        os.remove(instance.tracker.previous('mod_file').path)
        filename = random.randint(10000, 100000)**2
        filename = f"{slugify(instance.title)}_{str(filename)}.zip"
        os.rename(instance.mod_file.path, os.path.join(mod_file_folder, filename))
        instance.mod_file = f"mods/{str(instance.id)}/files/{filename}"
        instance.mod_file_size = os.path.getsize(os.path.join(mod_file_folder, filename)) 

        QuerySet(instance).filter(pk=instance.pk).update(
            mod_file=instance.mod_file,
            mod_file_size=instance.mod_file_size
        )
    elif instance.tracker.has_changed('mod_file') and created:
        filename = random.randint(10000, 100000)**2
        filename = f"{slugify(instance.title)}_{str(filename)}.zip"
        os.rename(instance.mod_file.path, os.path.join(mod_file_folder, filename))
        instance.mod_file = f"mods/{str(instance.id)}/files/{filename}"
        instance.mod_file_size = os.path.getsize(os.path.join(mod_file_folder, filename)) 

        QuerySet(instance).filter(pk=instance.pk).update(
            mod_file=instance.mod_file,
            mod_file_size=instance.mod_file_size
        )


@receiver(post_delete, sender=Mod)
def delete_mod(sender, instance, **kwargs):
    path = os.path.join(settings.MEDIA_ROOT, 'mods', str(instance.id))
    shutil.rmtree(path)


@receiver(post_save, sender=ModsGallery)
def screenshot_file_handler(sender, instance, created, **kwargs):
    path = os.path.join(settings.MEDIA_ROOT, 'mods', str(instance.mod.id), 'screenshots')
    filename = f"{random_digits(12)}.png"

    if not os.path.isdir(path):
        os.mkdir(path)
        os.mkdir(os.path.join(path, 'thumbnail'))

    # Move and place original image to folder
    os.rename(instance.image.path, os.path.join(path, filename))

    shutil.copyfile(os.path.join(path, filename), os.path.join(path, 'thumbnail', filename))

    img = Image.open(os.path.join(path, 'thumbnail', filename))
    if img.height > 250 or img.width > 250:
        output_size = (250, 250)
        img.thumbnail(output_size)
        img.save(os.path.join(path, 'thumbnail', filename))

    QuerySet(instance).filter(pk=instance.pk).update(
        image=f"mods/{str(instance.mod.id)}/screenshots/{filename}",
        image_thumb=f"mods/{str(instance.mod.id)}/screenshots/thumbnail/{filename}"
    )


@receiver(post_delete, sender=ModsGallery)
def screenshot_file_delete(sender, instance, **kwargs):
    os.remove(instance.image.path)
    os.remove(instance.image_thumb.path)


def random_digits(n):
    range_start = 10**(n-1)
    range_end = (10**n)-1
    return randint(range_start, range_end)