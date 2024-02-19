from django.db import models


class Category(models.Model):
    slug = models.SlugField(primary_key=True, blank=True)
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Article(models.Model):
    title = models.CharField(max_length=100)


class Test(models.Model):
    ...


class Collection(models.Model):
    slug = models.SlugField(primary_key=True, blank=True)
    articles = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='collection')
    tests = models.ForeignKey(Test, on_delete=models.CASCADE, related_name='test')

