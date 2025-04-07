from django.urls import path, include

from . import views

# Define the app name for URL namespacing
app_name = "blog"

urlpatterns = [
    # Route for the list of published posts
    path("", views.PostListView.as_view(), name="post_list"),
    # Route to filter posts by category name
    path(
        "category/<str:cat_name>/", views.PostListView.as_view(), name="post_category"
    ),
    # Route to filter posts by author's email
    path(
        "author/<str:author_email>/", views.PostListView.as_view(), name="post_author"
    ),
    # Route to view the details of a single post
    path("<int:pk>/", views.PostDetailView.as_view(), name="post_detail"),
    # Route to create a new post
    path("create/", views.PostCreateView.as_view(), name="post_create"),
    # Route to update an existing post
    path("<int:pk>/update/", views.PostUpdateView.as_view(), name="post_update"),
    # Route to delete a post
    path("<int:pk>/delete/", views.PostDeleteView.as_view(), name="post_delete"),
    # Route to manage posts that belong to the logged-in user
    path("manage_my_post/", views.ManagePostListView.as_view(), name="post_management"),
    # Route to list and create categories
    path("categories/", views.CategoryListCreateView.as_view(), name="category_list"),
    # Include API URLs from the blog's API version
    path("api/v1/", include("blog.api.v1.urls")),
]
