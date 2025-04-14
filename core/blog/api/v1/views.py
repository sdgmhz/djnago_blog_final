from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status
import requests
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page

from .serializers import PostSerializer, CategorySerializer, CryptoSerializer
from ...models import Post, Category
from .permissions import IsOwnerOrReadOnly, IsVerifiedOrReadOnly
from .paginations import CustomPagination


class PostModelViewSet(viewsets.ModelViewSet):
    """model viewset for implement CRUD for post"""

    serializer_class = PostSerializer
    permission_classes = [
        IsAuthenticatedOrReadOnly,
        IsOwnerOrReadOnly,
        IsVerifiedOrReadOnly,
    ]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = {
        "author": ["exact"],
        "category": ["exact"],
        "published_date": ["gt", "lt"],
    }
    search_fields = ["title", "content"]
    ordering_fields = ["counted_views", "published_date"]
    pagination_class = CustomPagination

    def get_queryset(self):
        return Post.objects.filter(
            status="pub", published_date__lte=timezone.now()
        ).prefetch_related("category")


class CategoryModelViewSet(viewsets.ModelViewSet):
    """model viewset for implement CRUD for category"""

    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsVerifiedOrReadOnly]
    pagination_class = CustomPagination
    queryset = Category.objects.all()


# Cache the API response for 60 seconds to reduce external API calls
@method_decorator(cache_page(60), name="dispatch")
class CryptoPriceApiView(GenericAPIView):
    """API view to retrieve the real-time price of a selected cryptocurrency."""

    serializer_class = CryptoSerializer

    def get(self, request):
        """Return instructions for using the API."""
        data = {
            "detail": "Please select a crypto from the list and the price will be shown. The result will be cached for 60 seconds"
        }
        return Response(data, status=status.HTTP_200_OK)

    def post(self, request):
        """Return the current price of the selected cryptocurrency."""
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        crypto_name = serializer.validated_data["crypto"]
        url = "https://api.wallex.ir/v1/markets"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()

            try:
                ask_price = data["result"]["symbols"][crypto_name]["stats"]["askPrice"]
                ask_price = float(ask_price)
            except KeyError as e:
                return Response(
                    {"detail": f"Key {e} not found in response."},
                    status=status.HTTP_404_NOT_FOUND,
                )
            symbol_to_name = dict(self.serializer_class.CRYPTO_CHOICES)
            crypto_label = symbol_to_name.get(crypto_name, crypto_name)
            return Response(
                {"detail": f"Price of {crypto_label} is {ask_price:.5f} US dollar"}
            )
        return Response(
            {"error": "Failed to fetch data from the server"},
            status=response.status_code,
        )
