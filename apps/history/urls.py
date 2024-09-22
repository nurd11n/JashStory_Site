from .views import *
from django.urls import path


urlpatterns = [
    path('category/', CategoryView.as_view()),
    path('category/<str:pk>/', CategoryView.as_view()),
    path('post/', PostView.as_view()),
    path('post/<str:pk>/', PostView.as_view()),
    path('year/', YearsView.as_view()),
    path('year/<str:pk>/', YearsView.as_view()),
    path('collection/', CollectionView.as_view()),
    path('collection/<str:pk>/', CollectionView.as_view()),
    path('search/', PostSearchView.as_view()),
    path('post/<int:pk>/recommendation/', PostRecommendationsApiView.as_view({'get': 'list'}), name='post-recommendation')
]