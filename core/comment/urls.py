from django.urls import path
from . import views

app_name = "comment"

urlpatterns = [
    path('', views.CommentListView.as_view(), name="comment_list"),
    path('<int:pk>/', views.CommentDetailView.as_view(), name="comment_detail"),
    path('<int:pk>/update/', views.CommentUpdateView.as_view(), name="comment_update"),
    path("<int:pk>/delete/", views.CommentDeleteView.as_view(), name="comment_delete"),

]