from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

from .serializers import PostSerializer, CategorySerializer
from ...models import Post, Category
from .permissions import IsOwnerOrReadOnly
from .paginations import CustomPagination


class PostModelViewSet(viewsets.ModelViewSet):
    """model viewset for implement CRUD for post"""
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = {'author':["exact"], 'category':["exact"], 'published_date':['gt', 'lt']}
    search_fields = ['title', 'content']
    ordering_fields = ['counted_views','published_date']
    pagination_class = CustomPagination

    def get_queryset(self):
        return Post.objects.filter(status='pub', published_date__lte=timezone.now()).prefetch_related('category')

class CategoryModelViewSet(viewsets.ModelViewSet):
    """model viewset for implement CRUD for category"""
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = CustomPagination
    queryset = Category.objects.all()