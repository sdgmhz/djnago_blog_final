from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django.shortcuts import get_object_or_404
from django.utils import timezone

from .serializers import PostSerializer
from ...models import Post
from .permissions import IsOwner



class PostModelViewSet(viewsets.ModelViewSet):
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwner]

    def get_queryset(self):
        return Post.objects.filter(status='pub', published_date__lte=timezone.now()).prefetch_related('category')
