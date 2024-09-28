from rest_framework import filters, generics, views, status, viewsets, mixins
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend
from .models import *
from .serializers import *
from .filters import PostFilter
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema
from django.db.models import Prefetch
from mixins.cache_mixin import CacheMixin
from .models import Post
from django.db.models import Q
from django.shortcuts import get_object_or_404


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


@extend_schema(tags=['Post Search'])
class PostSearchView(APIView):
    def get(self, request):
        query = request.GET.get('q')
        if query:
            posts = Post.objects.filter(title__icontains=query)
            serializer = PostSerializer(posts, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({"detail": "No query provided"}, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(tags=['Post Recommendation'])
class PostRecommendationsApiView(viewsets.GenericViewSet, mixins.ListModelMixin):
    serializer_class = PostSerializer

    def get_queryset(self):
        post_id = self.kwargs.get('pk')
        current_post = get_object_or_404(Post, id=post_id)
        title_words = current_post.title.split()
        query = Q()
        for word in title_words:
            query |= Q(title__icontains=word)
        queryset = Post.objects.filter(query).exclude(id=post_id)
        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
