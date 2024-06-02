from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from .models import *


class CategorySerializer(ModelSerializer):

    class Meta:
        model = Category
        fields = ['name', 'image']


class YearsSerializer(ModelSerializer):
    class Meta:
        model = Year
        fields = '__all__'

class PostListSerializer(ModelSerializer):
    images = serializers.SerializerMethodField("get_image")

    def get_image(self, obj):
        return PostImageSerializer(obj.images.all(), many=True).data
    
    class Meta:
        model = Post
        fields = ['category', 'title', 'years', 'collection', 'images']


class PostSerializer(ModelSerializer):
    images = serializers.SerializerMethodField("get_image")

    def get_image(self, obj):
        return PostImageSerializer(obj.images.all(), many=True).data
    
    class Meta:
        model = Post
        fields = ['category', 'title', 'years', 'article', 'collection', 'images']


class CollectionSerializer(ModelSerializer):
    images = serializers.SerializerMethodField("get_image")

    def get_image(self, obj):
        return CollectionImageSerializer(obj.images.all(), many=True).data
    
    class Meta:
        model = Collection
        fields = ['title', 'images']


class PostImageSerializer(ModelSerializer):

    class Meta:
        model = PostImage
        fields = ["image"]


class CollectionImageSerializer(ModelSerializer):

    class Meta:
        model = CollectionImage
        fields = ["image"]
