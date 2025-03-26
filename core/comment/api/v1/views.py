from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

from ...models import Comment
from .serializers import CommentSerializer
from .permissions import IsOwnerOrReadOnly
from .paginations import CustomPagination


class CommentModelViewSet(viewsets.ModelViewSet):
    """API viewset for managing comments with filtering, searching, and pagination."""
    queryset = Comment.objects.filter(approved=True)
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    serializer_class = CommentSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = {'post', 'recommend', 'email'}
    search_fields = ['subject', 'message']
    ordering_fields = ['created_date']
    pagination_class = CustomPagination

    def get_serializer_context(self):
        """Inject the request object into the serializer context."""
        context = super().get_serializer_context()
        context['request'] = self.request
        return context
