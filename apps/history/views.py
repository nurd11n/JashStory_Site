from rest_framework import filters, generics
from django_filters.rest_framework import DjangoFilterBackend
from .models import *
from .serializers import *


class CategoryView(generics.ListAPIView, generics.RetrieveAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['name']
    search_fields = ['name']


class YearsView(generics.ListAPIView):
    queryset = Year.objects.all()
    serializer_class = YearsSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['name', 'start_age', 'end_age']
    search_fields = ['name', 'start_age', 'end_age']


class PostView(generics.ListAPIView, generics.RetrieveAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['title', 'category', 'years', 'created_at']
    search_fields = ['title', 'years', 'category']


class CollectionView(generics.ListAPIView, generics.RetrieveAPIView):
    queryset = Collection.objects.all()
    serializer_class = CollectionSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['title']
    search_fields = ['title']


class PostImageViewSet(generics.ListAPIView):
    queryset = PostImage.objects.all()
    serializer_class = PostImageSerializer


class CollectionImageViewSet(generics.ListAPIView):
    queryset = CollectionImage.objects.all()
    serializer_class = CollectionImageSerializer