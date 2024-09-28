from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from .models import *


class PostImageSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    def get_image(self, obj):
        request = self.context.get('request')
        if request is not None:
            return request.build_absolute_uri(obj.image.url)
        else:
            return f'{settings.BASE_URL}{obj.image.url}'

    class Meta:
        model = PostImage 
        fields = ['image']


class CategorySerializer(ModelSerializer):

    class Meta:
        model = Category
        fields = ['id', 'name', 'image']


class YearsSerializer(ModelSerializer):
    class Meta:
        model = Year
        fields = '__all__'

class PostListSerializer(serializers.ModelSerializer):
    images = serializers.SerializerMethodField("get_image")

    def get_image(self, obj):
        return PostImageSerializer(obj.images.all(), many=True, context=self.context).data

    class Meta:
        model = Post
        fields = ['id', 'category', 'title', 'years', 'collection', 'images']


class PostSerializer(serializers.ModelSerializer):
    images = serializers.SerializerMethodField("get_image")

    def get_image(self, obj):
        return PostImageSerializer(obj.images.all(), many=True, context=self.context).data

    class Meta:
        model = Post
        fields = ['id', 'category', 'title', 'years', 'article', 'collection', 'images']


class CollectionSerializer(ModelSerializer):
    images = serializers.SerializerMethodField("get_image")

    def get_image(self, obj):
        return CollectionImageSerializer(obj.images.all(), many=True).data
    
    class Meta:
        model = Collection
        fields = ['id', 'title', 'images']


class CollectionImageSerializer(ModelSerializer):

    class Meta:
        model = CollectionImage
        fields = ["image"]
