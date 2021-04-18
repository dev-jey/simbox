
from django import template
from project_box.apps.mods.models import Type


register = template.Library()

@register.simple_tag
def categories(request):
    categories = Type.objects.all()
    return categories