import uuid
from PIL import Image
from io import BytesIO
from django.core.files import File
from django.core.files.base import ContentFile
from django.db import models


class ResizeImageMixin:
    def resize(self, imageField: models.ImageField, size: tuple):
        im = Image.open(imageField)  # Catch original
        source_image = im.convert('RGB')
        source_image.thumbnail(size)  # Resize to size

        # like you said, cut image dimensions in half
        w, h = source_image.size
        source_image = source_image.resize(size, Image.ANTIALIAS)

        output = BytesIO()

        source_image.save(output, format='JPEG')  # Save resize image to bytes
        image_size = output.tell()
        output.seek(0)

        content_file = ContentFile(output.read())  # Read output and create ContentFile in memory
        file = File(content_file)
        # imageField.save(random_name, file, save=False)
        return file
