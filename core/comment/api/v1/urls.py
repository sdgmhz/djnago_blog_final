from rest_framework.routers import DefaultRouter
from . import views

app_name = "api-v1"

""" create a router for comment urls """
router = DefaultRouter()
router.register("comments", views.CommentModelViewSet, basename="comment")
urlpatterns = router.urls
