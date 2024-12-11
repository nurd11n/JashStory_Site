from django.db import models

import uuid
import random
import string

from utils.fields import WEBPField, image_folder


def generate_unique_numeric_id():
    while True:
        unique_id = ''.join(random.choices(string.digits, k=10))
        if not Post.objects.filter(id=unique_id).exists():
            return unique_id


class Category(models.Model):
    id = models.CharField(primary_key=True, default=generate_unique_numeric_id, max_length=10, editable=False, unique=True)
    name = models.CharField(max_length=100, verbose_name="Наименование")
    image = WEBPField(upload_to=image_folder)

    fields_to_translate = ['name']

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

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Года'
        verbose_name_plural = 'Года'


class Collection(models.Model):
    id = models.CharField(primary_key=True, default=generate_unique_numeric_id, max_length=10, editable=False, unique=True)
    title = models.CharField(max_length=100, verbose_name="Наименование")
    image = WEBPField(upload_to=image_folder)

    fields_to_translate = ['title']

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Коллекция'
        verbose_name_plural = 'Коллекция'


class Post(models.Model):
    id = models.CharField(primary_key=True, default=generate_unique_numeric_id, max_length=10, editable=False, unique=True)
    category = models.ForeignKey(Category, models.CASCADE, related_name='posts')
    title = models.CharField(max_length=100)
    image = WEBPField(upload_to=image_folder)
    years = models.ForeignKey(Year, models.CASCADE, related_name='posts')
    article = models.TextField(null=True, blank=True)
    collection = models.ForeignKey(Collection, on_delete=models.CASCADE, related_name='posts')
    created_at = models.DateTimeField(auto_now_add=True)

    fields_to_translate = ['title', 'article']

    def __str__(self):
        return f'{self.title} - {self.years} - {self.category}'
    
    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Пост'


class Question(models.Model):
    text = models.TextField()
    

class Answer(models.Model):
    question = models.ForeignKey(Question, related_name='answers', on_delete=models.CASCADE)
    text = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)