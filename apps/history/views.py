from rest_framework.viewsets import ModelViewSet
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import *
from .serializers import *
from rest_framework.response import Response


class LanguageMixinForViews:
    def retrieve(self, request, *args, **kwargs):
        accept_language = request.headers.get('Accept-Language', 'en')
        instance = self.get_object()
        serializer = self.get_serializer(instance, accept_language=accept_language)
        return Response(serializer.data)


class CategoryView(ModelViewSet, LanguageMixinForViews):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['slug', 'name']
    search_fields = ['name']


class YearsView(ModelViewSet, LanguageMixinForViews):
    queryset = Years.objects.all()
    serializer_class = YearsSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['slug', 'ages']
    search_fields = ['ages']


class PostView(ModelViewSet, LanguageMixinForViews):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['title', 'category', 'years', 'created_at']
    search_fields = ['title', 'years', 'category']


class CollectionView(ModelViewSet, LanguageMixinForViews):
    queryset = Collection.objects.all()
    serializer_class = CollectionSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['slug', 'title']
    search_fields = ['title']