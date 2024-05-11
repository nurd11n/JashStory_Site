from rest_framework.serializers import ModelSerializer
from .models import *


class CategorySerializer(ModelSerializer):

    class Meta:
        model = Category
        fields = ['slug', 'name', 'image']


class YearsSerializer(ModelSerializer):
    class Meta:
        model = Years
        fields = '__all__'


class PostSerializer(ModelSerializer):
    class Meta:
        model = Post
        fields = ['category', 'title', 'years', 'article', 'collection', 'image']


class CollectionSerializer(ModelSerializer):
    class Meta:
        model = Collection
        fields = ['slug', 'title', 'image']


class PostImageSerializer(ModelSerializer):

    class Meta:
        model = PostImage
        fields = ["image"]


class CollectionImageSerializer(ModelSerializer):

    class Meta:
        model = CollectionImage
        fields = ["image"]
