from django.contrib import admin
from django import forms
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from .models import *
from mixins.translations_mixins import TranslatorMediaMixin

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
    list_display = ['slug', "name", ]
    list_display_links = ("slug", )
    prepopulated_fields = {'slug': ("name", )}


class PostImageInline(admin.TabularInline):
    model = PostImage
    max_num = 20
    extra = 0


@admin.register(Post)
class PostAdminModel(TranslatorMediaMixin):
    inlines = [PostImageInline, ]
    list_display = ["title", ]


class CollectionImageInline(admin.TabularInline):
    model = CollectionImage
    max_num = 20
    extra = 0


@admin.register(Collection)
class CollectionAdminModel(TranslatorMediaMixin):
    inlines = [CollectionImageInline, ]
    list_display = ["title", ]


admin.site.register(Years)

