from django.contrib import admin
from django import forms
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from .models import *
from mixins.translations_mixins import TranslatorMediaMixin
from .filters import PostFilter

TEXT = "Здесь вам нужно будет ввести данные товара на 3 разных языках"


class PostAdminForm(forms.ModelForm):
    description_ru = forms.CharField(label="Описание", widget=CKEditorUploadingWidget())
    description_en = forms.CharField(label="Описание", widget=CKEditorUploadingWidget())
    description_ky = forms.CharField(label="Описание", widget=CKEditorUploadingWidget())

    class Meta:
        model = Post
        fields = '__all__'


@admin.register(Category)
class CategoryAdminModel(TranslatorMediaMixin):
    list_display = ['id', "name", ]
    list_display_links = ("id",)
    list_filter = ['id', "name"]
    search_fields = ['id', "name"]


@admin.register(Post)
class PostAdminModel(TranslatorMediaMixin):
    list_display = ['id', "title", ]
    list_display_links = ("id",)
    list_filter = ['id', "title"]
    filter_class = PostFilter
    search_fields = ['id', "title"]


@admin.register(Collection)
class CollectionAdminModel(TranslatorMediaMixin):
    list_display = ['id', "title", ]
    list_display_links = ("id",)
    list_filter = ['id', "title"]
    search_fields = ['id', "title"]


admin.site.register(Year)

