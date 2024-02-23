from django.db import models


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


class Post(models.Model):
    category = models.ForeignKey(Category, models.CASCADE, related_name='posts')
    title = models.CharField(max_length=100)
    years = models.ForeignKey(Years, models.CASCADE, related_name='posts')
    article = models.TextField()
    image = models.ImageField(upload_to='images/', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.title} - {self.years} - {self.category}'


class Collection(models.Model):
    slug = models.SlugField(primary_key=True, blank=True)
    title = models.CharField(max_length=100, unique=True)
    image = models.ImageField(upload_to='images/', blank=True)
    posts = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='collection')

    def __str__(self):
        return self.title




