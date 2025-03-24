from django.urls import path
from rest_framework.routers import DefaultRouter

from . import views

app_name = 'api-v1'

""" create a router for post and category urls"""
router = DefaultRouter()
router.register('post', views.PostModelViewSet, basename='post')
router.register('category', views.CategoryModelViewSet, basename='category')
urlpatterns = router.urls


