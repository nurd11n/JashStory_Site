from django.db import models
from ckeditor.fields import RichTextField

import uuid
import random
import string


from mixins.model_translation import TranslationMixin
from utils.fields import WEBPField, image_folder


def generate_unique_numeric_id():
    while True:
        unique_id = ''.join(random.choices(string.digits, k=10))
        if not Post.objects.filter(id=unique_id).exists():
            return unique_id


class Category(TranslationMixin, models.Model):
    id = models.CharField(primary_key=True, default=generate_unique_numeric_id, max_length=10, editable=False, unique=True)
    name = models.CharField(max_length=100, verbose_name="Наименование")
    image = WEBPField(upload_to=image_folder)

    fields_to_translate = ['name']
    CACHE_KEY_PREFIX = "category"

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категория'


class Year(models.Model):
    id = models.CharField(primary_key=True, default=generate_unique_numeric_id, max_length=10, editable=False, unique=True)
    name = models.CharField(max_length=100, verbose_name="Наименование")
    start_age = models.IntegerField(blank=True, null=True)
    end_age = models.IntegerField(blank=True, null=True)

    CACHE_KEY_PREFIX = "year"

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Года'
        verbose_name_plural = 'Года'


class Collection(TranslationMixin, models.Model):
    id = models.CharField(primary_key=True, default=generate_unique_numeric_id, max_length=10, editable=False, unique=True)
    title = models.CharField(max_length=100, verbose_name="Наименование")

    fields_to_translate = ['title']
    CACHE_KEY_PREFIX = "collection"

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Коллекция'
        verbose_name_plural = 'Коллекция'


class CollectionImage(models.Model):
    collection = models.ForeignKey(Collection, related_name='images', on_delete=models.CASCADE)
    image = WEBPField(upload_to=image_folder)

    CACHE_KEY_PREFIX = "collection_image"


class Post(TranslationMixin, models.Model):
    id = models.CharField(primary_key=True, default=generate_unique_numeric_id, max_length=10, editable=False, unique=True)
    category = models.ForeignKey(Category, models.CASCADE, related_name='posts')
    title = models.CharField(max_length=100)
    years = models.ForeignKey(Year, models.CASCADE, related_name='posts')
    article = RichTextField(null=True, blank=True)
    collection = models.ForeignKey(Collection, on_delete=models.CASCADE, related_name='posts')
    created_at = models.DateTimeField(auto_now_add=True)

    fields_to_translate = ['title', 'article']
    CACHE_KEY_PREFIX = "post"

    def __str__(self):
        return f'{self.title} - {self.years} - {self.category}'
    
    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Пост'
    

class PostImage(models.Model):
    post = models.ForeignKey(Post, related_name='images', on_delete=models.CASCADE)
    image = WEBPField(upload_to=image_folder)

    CACHE_KEY_PREFIX = "post_image"

