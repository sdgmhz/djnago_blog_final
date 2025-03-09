from django.urls import path

from . import views

app_name = "blog"

urlpatterns = [
    path('', views.PostListView.as_view(), name="post_list"),
    path('category/<str:cat_name>/', views.PostListView.as_view(), name='post_category'),
    path('author/<str:author_email>/', views.PostListView.as_view(), name='post_author'),
    
    path('<int:pk>/', views.PostDetailView.as_view(), name="post_detail"),
]