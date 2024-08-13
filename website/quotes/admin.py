from django.contrib import admin
from .models import Quote, Tag, Author, FileImage
from unfold.admin import ModelAdmin
from imagekit.admin import AdminThumbnail
from django.db import models
from unfold.contrib.forms.widgets import WysiwygWidget


class QuoteStatusFilter(admin.SimpleListFilter):
    title = 'Status'
    parameter_name = 'status'

    def lookups(self, request, model_admin):
        return [
            ('published', 'Published'),
            ('draft', 'Draft'),
        ]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.distinct().filter(status=self.value())
        return queryset.distinct().all()


@admin.register(Quote)
class QuoteAdmin(ModelAdmin):
    readonly_fields = (
        'updated_at',)
    list_display = ('title', 'author', 'tagss', 'explicit_text', 'created_at', 'updated_at')
    search_fields = ('title', 'body', 'author__name')
    list_filter = (
        QuoteStatusFilter, )
    autocomplete_fields = ['author', 'tags', 'file_image']

    widgets = {
        'analyze': WysiwygWidget,
    }

    formfield_overrides = {
        models.TextField: {
            "widget": WysiwygWidget,
        }
    }

    def tagss(self, obj):
        return ",".join([q.name for q in obj.tags.all()])

    class Media:
        pass


@admin.register(Author)
class AuthorAdmin(ModelAdmin):
    readonly_fields = ('updated_at',)
    search_fields = ['name']
    list_display = ('name','created_at','updated_at','image')

    widgets = {
        'analyze': WysiwygWidget,
    }

    formfield_overrides = {
        models.TextField: {
            "widget": WysiwygWidget,
        }
    }

@admin.register(Tag)
class TagAdmin(ModelAdmin):
    readonly_fields = ('updated_at',)
    search_fields = ['name']
    list_display = ('name',)


@admin.register(FileImage)
class FileImageAdmin(ModelAdmin):
    readonly_fields = ('updated_at',)
    thumbnail_preview = AdminThumbnail(image_field='file')
    list_display = ('uuid', 'thumbnail_preview' )
    search_fields = ['uuid']