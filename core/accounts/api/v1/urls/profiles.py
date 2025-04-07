from django.urls import path

from .. import views

urlpatterns = [
    # Route to profile view
    path("", views.ProfileApiView.as_view(), name="profile"),
]
