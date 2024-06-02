from rest_framework import filters, generics, views, status
from django_filters.rest_framework import DjangoFilterBackend
from .models import *
from .serializers import *
from .filters import PostFilter
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema
from django.db.models import Prefetch
from mixins.cache_mixin import CacheMixin


@extend_schema(tags=['Category'])
class CategoryView(CacheMixin, generics.ListAPIView, generics.RetrieveAPIView):
    CACHE_KEY_PREFIX = "catalogue"
    queryset = Category.objects.prefetch_related('posts')
    serializer_class = CategorySerializer
    filter_backends = [filters.SearchFilter, DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['name']
    search_fields = ['name']


@extend_schema(tags=['Years'])
class YearsView(CacheMixin, generics.ListAPIView):
    CACHE_KEY_PREFIX = "year"
    queryset = Year.objects.prefetch_related('posts')
    serializer_class = YearsSerializer
    filter_backends = [filters.SearchFilter, DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['name', 'start_age', 'end_age']
    search_fields = ['name', 'start_age', 'end_age']


@extend_schema(tags=['Posts'])
class PostView(CacheMixin, generics.ListAPIView, generics.RetrieveAPIView):
    CACHE_KEY_PREFIX = "post"
    queryset = Post.objects.all().select_related("years", 'collection', 'category').prefetch_related(
        Prefetch("images"),
        Prefetch("years"),
        Prefetch("category"),
        Prefetch("collection"),
    )
    serializer_class = PostSerializer
    filter_backends = [filters.SearchFilter, DjangoFilterBackend, filters.OrderingFilter]
    filterset_class = PostFilter
    search_fields = ['title', 'years', 'category']

    def get_serializer_class(self):
        if "pk" in self.kwargs:
            return PostSerializer
        return PostListSerializer
    
    def get(self, request, *args, **kwargs):
        if "pk" in self.kwargs:
            return self.retrieve(request, *args, **kwargs)
        return self.list(request, *args, **kwargs)


@extend_schema(tags=['Collections'])
class CollectionView(CacheMixin, generics.ListAPIView, generics.RetrieveAPIView):
    CACHE_KEY_PREFIX = "collection"
    queryset = Collection.objects.prefetch_related('posts')
    serializer_class = CollectionSerializer
    filter_backends = [filters.SearchFilter, DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['title']
    search_fields = ['title']


@extend_schema(tags=['Post - Image'])
class PostImageViewSet(CacheMixin, generics.ListAPIView):
    CACHE_KEY_PREFIX = "post_image"
    queryset = PostImage.objects.all()
    serializer_class = PostImageSerializer


@extend_schema(tags=['Collections - Image'])
class CollectionImageViewSet(CacheMixin, generics.ListAPIView):
    CACHE_KEY_PREFIX = "collection_image"
    queryset = CollectionImage.objects.all()
    serializer_class = CollectionImageSerializer