from rest_framework.viewsets import ModelViewSet
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import *
from .serializers import *
from rest_framework import generics


class CategoryView(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['slug', 'name']
    search_fields = ['name']


class YearsView(ModelViewSet):
    queryset = Years.objects.all()
    serializer_class = YearsSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['slug', 'ages']
    search_fields = ['ages']


class PostView(ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['title', 'category', 'years', 'created_at']
    search_fields = ['title', 'years', 'category']


class CollectionView(ModelViewSet):
    queryset = Collection.objects.all()
    serializer_class = CollectionSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['slug', 'title']
    search_fields = ['title']


class PostImageViewSet(generics.ListAPIView):
    queryset = PostImage.objects.all()
    serializer_class = PostImageSerializer


class CollectionImageViewSet(generics.ListAPIView):
    queryset = CollectionImage.objects.all()
    serializer_class = CollectionImageSerializer