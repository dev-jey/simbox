from django.contrib import admin
from .models import (
    Mod,
    Simulator,
    ModsType,
    ModsLike,
    ModsView,
    ModsGallery,
    ModsListName,
    ModsListConnector,
    ModComments,
    ModsDownloadsCounter
)


class ModsViewsAdmin(admin.ModelAdmin):
    list_display = (
        'mod_id',
        'IPAddress'
    )


class ModsGalleryAdmin(admin.StackedInline):
    model = ModsGallery
    max_num = 12
    exclude = ("image_thumb",)


class ModAdmin(admin.ModelAdmin):
    exclude = ("mod_file_size",)
    inlines = [ModsGalleryAdmin]
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


class ModsLikeViewsAdmin(admin.ModelAdmin):
    list_display = (
        'mod_id',
        'user_id',
        'datetime_liked'
    )


class SimulatorViewsAdmin(admin.ModelAdmin):
    list_display = (
        'simulator',
    )


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


class ModListNameAdmin(admin.ModelAdmin):
    model = ModsListName
    search_fields = ['list_name', 'list_owner__username']
    list_display = (
        "list_name",
        "list_owner",
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


class ModsListConnectorAdmin(admin.ModelAdmin):
    model = ModsListConnector
    list_display = (
        "list_id",
        "mod_id",
        "user_id",
        "datetime_created"
    )


admin.site.register(Mod, ModAdmin)
# admin.site.register(ModsGallery, ModsGalleryAdmin)
admin.site.register(Simulator, SimulatorViewsAdmin)
admin.site.register(ModsType)
admin.site.register(ModsLike, ModsLikeViewsAdmin)
admin.site.register(ModsView, ModsViewsAdmin)
admin.site.register(ModsListName, ModListNameAdmin)
admin.site.register(ModsListConnector, ModsListConnectorAdmin)
admin.site.register(ModComments, ModCommentsAdmin)
admin.site.register(ModsDownloadsCounter, ModsDownloadsCounterAdmin)
