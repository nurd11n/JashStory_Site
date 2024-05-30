from django.db import models
from googletrans import Translator, LANGUAGES
import asyncio

translator = Translator()


class TranslationMixin:
    fields_to_translate = []

    async def translate_text(self, text, lang):
        translated_text = await asyncio.sleep(0, translator.translate(text, src='ru', dest=lang))
        return translated_text.text

    async def translate_fields(self):
        tasks = []
        for field_name in self.fields_to_translate:
            text = getattr(self, field_name)
            languages = ['en', 'ky', 'zh-tw']
            tasks.extend([self.translate_text(text, lang) for lang in languages])
        translations = await asyncio.gather(*tasks)
        for i, field_name in enumerate(self.fields_to_translate):
            for j, lang in enumerate(languages):
                translated_text = translations[i * len(languages) + j]
                setattr(self, f"{field_name}_{lang}" if lang != 'zh-tw' else f"{field_name}_zh_hant", translated_text)

    def save(self, *args, **kwargs):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.translate_fields())
        super().save(*args, **kwargs)


class Category(TranslationMixin, models.Model):
    slug = models.SlugField(primary_key=True, blank=True, unique=True)
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='images/', blank=True)

    fields_to_translate = ['name']

    def __str__(self):
        return self.name


class Year(models.Model):
    name = models.CharField(max_length=100)
    start_age = models.IntegerField(blank=True, null=True)
    end_age = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.name


class Collection(TranslationMixin, models.Model):
    slug = models.SlugField(primary_key=True, blank=True, unique=True)
    title = models.CharField(max_length=100)

    fields_to_translate = ['title']

    def __str__(self):
        return self.title
    

class CollectionImage(models.Model):
    collection = models.ForeignKey(Collection, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='collection_images/')


class Post(TranslationMixin, models.Model):
    category = models.ForeignKey(Category, models.CASCADE, related_name='posts')
    title = models.CharField(max_length=100)
    years = models.ForeignKey(Year, models.CASCADE, related_name='posts')
    article = models.TextField()
    collection = models.ForeignKey(Collection, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    fields_to_translate = ['title', 'article']

    def __str__(self):
        return f'{self.title} - {self.years} - {self.category}'
    

class PostImage(models.Model):
    post = models.ForeignKey(Post, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='post_images/')

