from django.contrib import admin
from .models import (
    Mod,
    ModsType,
    ModComments,
    ModsDownloadsCounter
)


class ModAdmin(admin.ModelAdmin):
    exclude = ("mod_file_size",)
    list_display = (
        'id',
        'title',
        'visible',
        'verified',
        'author',
        'datetime_created',
        'datetime_updated'
    )
    search_fields = ['title']
    readonly_fields = ["author"]

    def save_model(self, request, obj, form, change):
        if not obj.id:
            obj.author = request.user
        super(ModAdmin, self).save_model(request, obj, form, change)

    class Meta:
        model = Mod



class ModCommentsAdmin(admin.ModelAdmin):
    model = ModComments
    search_fields = ['user_id__username']
    list_display = (
        "user_id",
        "mod_id",
        "visible",
        "datetime_created",
        "datetime_updated"
    )


class ModsDownloadsCounterAdmin(admin.ModelAdmin):
    model = ModsDownloadsCounter
    list_display = (
        "mod_id",
        "IPAddress",
        "datetime_created"
    )


admin.site.register(Mod, ModAdmin)
admin.site.register(ModsType)
admin.site.register(ModComments, ModCommentsAdmin)
admin.site.register(ModsDownloadsCounter, ModsDownloadsCounterAdmin)
