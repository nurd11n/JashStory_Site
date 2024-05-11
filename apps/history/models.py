from django.db import models
from googletrans import Translator, LANGUAGES
import asyncio


class TranslationMixin:
    fields_to_translate = []

    async def translate_fields(self):
        translator = Translator()
        tasks = await asyncio.gather(*map(lambda field_name: self.translate_text(translator, field_name, getattr(self, field_name)), self.fields_to_translate))
        translations = [translation for translation_list in tasks for translation in translation_list]
        for field_name, lang, translated_text in translations:
            setattr(self, f"{field_name}_{lang}" if lang != 'zh-tw' else f"{field_name}_zh_hant", translated_text)

    @staticmethod
    async def translate_text(translator, field_name, text):
        languages = ['en', 'ky', 'zh-tw']
        translations = []
        for lang in languages:
            translated_text = await asyncio.to_thread(translator.translate, text, src='ru', dest=lang)
            translations.append((field_name, lang, translated_text.text))
        return translations

    def save(self, *args, **kwargs):
        asyncio.run(self.translate_fields())
        super().save(*args, **kwargs)


class Category(TranslationMixin, models.Model):
    slug = models.SlugField(primary_key=True, blank=True, unique=True)
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='images/', blank=True)

    fields_to_translate = ['name']

    def __str__(self):
        return self.name


class Years(models.Model):
    slug = models.SlugField(primary_key=True, blank=True, unique=True)
    ages = models.DateField()

    def __str__(self):
        return self.ages.year


class Collection(TranslationMixin, models.Model):
    slug = models.SlugField(primary_key=True, blank=True, unique=True)
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='images/', blank=True)

    fields_to_translate = ['title']

    def __str__(self):
        return self.title
    

class CollectionImage(models.Model):
    auto = models.ForeignKey(Collection, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='collection_images/')


class Post(TranslationMixin, models.Model):
    category = models.ForeignKey(Category, models.CASCADE, related_name='posts')
    title = models.CharField(max_length=100)
    years = models.ForeignKey(Years, models.CASCADE, related_name='posts')
    article = models.TextField()
    image = models.ImageField(upload_to='images/', blank=True)
    collection = models.ForeignKey(Collection, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    fields_to_translate = ['title', 'article']

    def __str__(self):
        return f'{self.title} - {self.years} - {self.category}'
    

class PostImage(models.Model):
    auto = models.ForeignKey(Post, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='post_images/')

