from django.contrib import admin
from .models import (
    Mod,
    SubType,
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

    class Meta:
        model = Mod


class SubTypeAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'created_at',
        'updated_at'
    )
    search_fields = ['name']

    class Meta:
        model = SubType


class TypesAdmin(admin.ModelAdmin):
    model = Type
    search_fields = ['name']
    list_display = (
        "name",
        "created_at",
        "updated_at"
    )


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
admin.site.register(Type, TypesAdmin)
admin.site.register(Comment, ModCommentsAdmin)
admin.site.register(Download, ModsDownloadsCounterAdmin)
admin.site.register(SubType, SubTypeAdmin)
