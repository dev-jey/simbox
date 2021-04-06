from django.contrib import admin
from .models import News


class NewsAdmin(admin.ModelAdmin):
    model = News
    list_display = ("title", "visible", "author", "datetime_created")
    search_fields = ["title"]
    readonly_fields = ["author"]

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.author = request.user  # FIXME: ONLY SAVE AUTHOR ON CREATION

        super(NewsAdmin, self).save_model(request, obj, form, change)


admin.site.register(News, NewsAdmin)
