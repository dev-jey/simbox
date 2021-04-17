from django.contrib import admin
from .models import (
    Mod,
    Type,
    Comment,
    Download
)


class ModAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'title',
        'visible',
        'verified',
        'created_at',
        'updated_at'
    )
    search_fields = ['title']

    def save_model(self, request, obj, form, change):
        if not obj.id:
            obj.author = request.user
        super(ModAdmin, self).save_model(request, obj, form, change)

    class Meta:
        model = Mod


class ModCommentsAdmin(admin.ModelAdmin):
    model = Comment
    search_fields = ['user_id__username']
    list_display = (
        "visible",
        "created_at",
        "updated_at"
    )


class ModsDownloadsCounterAdmin(admin.ModelAdmin):
    model = Download
    list_display = (
        "ip_address",
        "created_at"
    )


admin.site.register(Mod, ModAdmin)
admin.site.register(Type)
admin.site.register(Comment, ModCommentsAdmin)
admin.site.register(Download, ModsDownloadsCounterAdmin)
