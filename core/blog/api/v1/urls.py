from rest_framework.routers import DefaultRouter
from django.urls import path

from . import views

app_name = "api-v1"

""" create a router for post and category urls"""
router = DefaultRouter()
router.register("post", views.PostModelViewSet, basename="post")
router.register("category", views.CategoryModelViewSet, basename="category")
urlpatterns = router.urls

urlpatterns += [
    # Route to crypto price API endpoint
    path("crypto-price/", views.CryptoPriceApiView.as_view(), name="crypto-price"),
]
