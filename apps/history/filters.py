from django_filters import FilterSet, RangeFilter, NumberFilter
from .models import Post


class PostFilter(FilterSet):
    class Meta:
        model = Post
        fields = ['title', 'category', 'years', 'created_at']
        
        