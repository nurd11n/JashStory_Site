from django.db import models
from googletrans import Translator
import asyncio


class TranslationMixin:
    fields_to_translate = []

    async def translate_fields(self):
        translator = Translator()
        tasks = []
        for field_name in self.fields_to_translate:
            field_value = getattr(self, field_name)
            tasks.append(self.translate_text(translator, field_name, field_value))
        translated_texts = await asyncio.gather(*tasks)
        for field_name, translations in translated_texts:
            for lang, translated_text in translations.items():
                setattr(self, f"{field_name}_{lang}", translated_text)

    @staticmethod
    async def translate_text(translator, field_name, text):
        translations = {}
        languages = ['en', 'ky']
        for lang in languages:
            translated_text = await asyncio.to_thread(
                translator.translate, text, src='ru', dest=lang
            )
            translations[lang] = translated_text.text
        return field_name, translations

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

