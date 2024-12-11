from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from .models import *


class CategorySerializer(ModelSerializer):

    class Meta:
        model = Category
        fields = ['id', 'name', 'image']


class YearsSerializer(ModelSerializer):
    class Meta:
        model = Year
        fields = '__all__'


class CollectionSerializer(ModelSerializer):
    
    class Meta:
        model = Collection
        fields = ['id', 'title', 'image']


class PostListSerializer(serializers.ModelSerializer):
    category = CategorySerializer() 
    years = YearsSerializer()        
    collection = CollectionSerializer()

    class Meta:
        model = Post
        fields = ['id', 'category', 'title', 'years', 'collection', 'image']


class PostSerializer(serializers.ModelSerializer):
    category = CategorySerializer()  
    years = YearsSerializer()        
    collection = CollectionSerializer()

    class Meta:
        model = Post
        fields = ['id', 'category', 'title', 'years', 'article', 'collection', 'image']


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ['id', 'text', 'is_correct']
        

class QuestionSerializer(serializers.ModelSerializer):
    answers = AnswerSerializer(many=True)

    class Meta:
        model = Question
        fields = ['id', 'text', 'answers']