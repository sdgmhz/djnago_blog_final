from django.shortcuts import get_object_or_404
from django.views.generic import ListView, DetailView
from django.utils import timezone

from .models import Post


class PostListView(ListView):
    context_object_name = "posts"
    template_name = 'blog/post_list.html'
    paginate_by = 4

    def get_queryset(self):
        posts = Post.objects.filter(status="pub", published_date__lte=timezone.now()).order_by('published_date')
        cat_name = self.kwargs.get('cat_name')
        author_email = self.kwargs.get('author_email')
        if cat_name:
            posts = posts.filter(category__name=cat_name)
        if author_email:
            posts = posts.filter(author__user__email=author_email)
        return posts

class PostDetailView(DetailView):
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'
    queryset = Post.objects.filter(status='pub', published_date__lte=timezone.now())

