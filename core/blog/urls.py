from django.urls import path

from . import views

app_name = "blog"

urlpatterns = [
    path('', views.PostListView.as_view(), name="post_list"),
    path('category/<str:cat_name>/', views.PostListView.as_view(), name='post_category'),
    path('author/<str:author_email>/', views.PostListView.as_view(), name='post_author'),
    
    path('<int:pk>/', views.PostDetailView.as_view(), name="post_detail"),

    path('create/', views.PostCreateView.as_view(), name="post_create"),
    path('<int:pk>/update/', views.PostUpdateView.as_view(), name="post_update"),
    path('<int:pk>/delete/', views.PostDeleteView.as_view(), name="post_delete"),
]