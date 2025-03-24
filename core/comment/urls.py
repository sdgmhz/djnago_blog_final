from django.urls import path, include
from . import views

app_name = "comment"

urlpatterns = [
    # Route to display a list of comments.
    path('', views.CommentListView.as_view(), name="comment_list"),

    # Route to display the details of a specific comment
    path('<int:pk>/', views.CommentDetailView.as_view(), name="comment_detail"),

    # Route to update an existing comment.
    path('<int:pk>/update/', views.CommentUpdateView.as_view(), name="comment_update"),

    # Route to delete a comment
    path("<int:pk>/delete/", views.CommentDeleteView.as_view(), name="comment_delete"),

    # Include API URLs from the comments's API version
    path('api/v1/', include('comment.api.v1.urls')),

]