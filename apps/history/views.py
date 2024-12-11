from rest_framework import filters, generics, views, status, viewsets, mixins
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend
from .models import *
from .serializers import *
from .filters import PostFilter
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema
from django.db.models import Prefetch
from .models import Post
from django.db.models import Q
from django.shortcuts import get_object_or_404


@extend_schema(tags=['Category'])
class CategoryView(generics.ListAPIView, generics.RetrieveAPIView):
    queryset = Category.objects.prefetch_related('posts')
    serializer_class = CategorySerializer
    filter_backends = [filters.SearchFilter, DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['name']
    search_fields = ['name']


@extend_schema(tags=['Years'])
class YearsView(generics.ListAPIView):
    queryset = Year.objects.prefetch_related('posts')
    serializer_class = YearsSerializer
    filter_backends = [filters.SearchFilter, DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['name', 'start_age', 'end_age']
    search_fields = ['name', 'start_age', 'end_age']


@extend_schema(tags=['Posts'])
class PostView(generics.ListAPIView, generics.RetrieveAPIView):
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
class CollectionView(generics.ListAPIView, generics.RetrieveAPIView):
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


class QuestionListCreateAPIView(generics.ListCreateAPIView):
    queryset = Question.objects.prefetch_related('answers').all()
    serializer_class = QuestionSerializer


class QuestionRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Question.objects.prefetch_related('answers').all()
    serializer_class = QuestionSerializer


class SubmitTestAPIView(generics.GenericAPIView):
    def post(self, request, *args, **kwargs):
        answers = request.data.get('answers', [])
        correct_count = 0
        total_questions = 0

        for answer in answers:
            question_id = answer.get('question_id')
            answer_id = answer.get('answer_id')

            try:
                question = Question.objects.get(id=question_id)
                selected_answer = question.answers.get(id=answer_id)
                total_questions += 1
                if selected_answer.is_correct:
                    correct_count += 1
            except (Question.DoesNotExist, Answer.DoesNotExist):
                return Response({"error": "Invalid question or answer ID"}, status=400)

        return Response({
            "total_questions": total_questions,
            "correct_answers": correct_count,
            "score": f"{correct_count}/{total_questions}"
        })