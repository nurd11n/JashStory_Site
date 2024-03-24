from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from googletrans import Translator


class Category(models.Model):
    slug = models.SlugField(primary_key=True, blank=True)
    name = models.CharField(max_length=100, unique=True)
    image = models.ImageField(upload_to='images/', blank=True)

    def __str__(self):
        return self.name


class Years(models.Model):
    slug = models.SlugField(primary_key=True, blank=True)
    ages = models.DateField(unique=True)

    def __str__(self):
        return self.ages.year


class Collection(models.Model):
    slug = models.SlugField(primary_key=True, blank=True)
    title = models.CharField(max_length=100, unique=True)
    image = models.ImageField(upload_to='images/', blank=True)

    def __str__(self):
        return self.title


class Post(models.Model):
    category = models.ForeignKey(Category, models.CASCADE, related_name='posts')
    title = models.CharField(max_length=100)
    years = models.ForeignKey(Years, models.CASCADE, related_name='posts')
    article = models.TextField()
    image = models.ImageField(upload_to='images/', blank=True)
    collection = models.ForeignKey(Collection, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.title} - {self.years} - {self.category}'


@receiver(pre_save, sender=Category)
@receiver(pre_save, sender=Collection)
@receiver(pre_save, sender=Post)
def translate_fields(sender, instance, **kwargs):
    translator = Translator()
    fields_to_translate = []
    
    if sender == Collection:
        fields_to_translate = ['title']
    elif sender == Category:
        fields_to_translate = ['name']
    elif sender == Post:
        fields_to_translate = ['title', 'article']
    
    for field_name in fields_to_translate:
        field_value = getattr(instance, field_name)
        try:
            translated_text_en = translator.translate(field_value, src='ru', dest='en').text
            translated_text_ky = translator.translate(field_value, src='ru', dest='ky').text
            translated_text_zh_hant = translator.translate(field_value, src='ru', dest='zh-tw').text
            setattr(instance, field_name + '_ru', field_value)
            setattr(instance, field_name + '_en', translated_text_en)
            setattr(instance, field_name + '_ky', translated_text_ky)
            setattr(instance, field_name + '_zh_hant', translated_text_zh_hant)
        except (AttributeError, ValueError, IndexError, ConnectionError) as e:
            print(f"Translation error: {e}")


