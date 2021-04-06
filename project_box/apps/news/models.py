from django.db import models
from tinymce.models import HTMLField
from django.conf import settings


class News(models.Model):
    title = models.CharField(max_length=120)
    text = HTMLField(max_length=10000)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        blank=True,
        editable=False,
        on_delete=models.CASCADE
    )
    visible = models.BooleanField(default=False)
    datetime_created = models.DateTimeField(auto_now_add=True)
    datetime_updated = models.DateTimeField(auto_now=True)
