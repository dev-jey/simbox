from project_box.apps.mods.models import Type


def categories_processor(request):
    categories = Type.objects.all()
    return {
        'categories': categories
    }
