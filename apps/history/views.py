from rest_framework.viewsets import ModelViewSet
from .models import *
from .serializers import *


class CategoryView(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class YearsView(ModelViewSet):
    queryset = Years.objects.all()
    serializer_class = YearsSerializer


class PostView(ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer


class CollectionView(ModelViewSet):
    queryset = Collection.objects.all()
    serializer_class = CollectionSerializer