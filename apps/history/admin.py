from django.contrib import admin
from django import forms
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from .models import *

TEXT = "Здесь вам нужно будет ввести данные товара на 3 разных языках"


class AutoAdminForm(forms.ModelForm):
    description_ru = forms.CharField(label="Описание", widget=CKEditorUploadingWidget())
    description_en = forms.CharField(label="Описание", widget=CKEditorUploadingWidget())
    description_ky = forms.CharField(label="Описание", widget=CKEditorUploadingWidget())

    class Meta:
        model = Post
        fields = '__all__'


@admin.register(Category)
class CategoryAdminModel(admin.ModelAdmin):
    list_display = ['slug', "name", ]
    list_display_links = ("slug", )
    prepopulated_fields = {'slug': ("name", )}

    fieldsets = (
        ('Base Fields', {
            'fields': ("slug", 'name', 'image'),
            'description': '%s' % TEXT,
        }),
        ('Russian Language', {
            'fields': ('name_ru',),
        }),
        ('English Language', {
            'fields': ('name_en',),
        }),
        ('Kyrgyz Language', {
            'fields': ('name_ky',),
        }),
    )


@admin.register(Post)
class PostAdminModel(admin.ModelAdmin):

    fieldsets = (
        ('Base Fields', {
            'fields': ('category', 'image', 'title', 'years', 'article', 'collection'),
            'description': '%s' % TEXT,
        }),
        ('Russian Language', {
            'fields': ('title_ru', 'article_ru',),
        }),
        ('English Language', {
            'fields': ('title_en', 'article_en',),
        }),
        ('Kyrgyz Language', {
            'fields': ('title_ky', 'article_ky',),
        }),
    )


@admin.register(Collection)
class CollectionAdminModel(admin.ModelAdmin):
    list_display = ['slug', "title", ]
    list_display_links = ("slug", )
    prepopulated_fields = {'slug': ("title", )}

    fieldsets = (
        ('Base Fields', {
            'fields': ('slug', 'title',),
            'description': '%s' % TEXT,
        }),
        ('Russian Language', {
            'fields': ('title_ru',),
        }),
        ('English Language', {
            'fields': ('title_en',),
        }),
        ('Kyrgyz Language', {
            'fields': ('title_ky',),
        }),
    )


admin.site.register(Years)

