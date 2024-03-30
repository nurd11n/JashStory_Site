from .views import *
from django.urls import path, include
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register('categories', CategoryView)
router.register('years', YearsView)
router.register('posts', PostView)
router.register('collections', CollectionView)

urlpatterns = [
    path('', include(router.urls)),
]