from django.shortcuts import get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.utils import timezone
from django.urls import reverse_lazy
from django.contrib import messages

from .models import Post
from accounts.models import Profile


class PostListView(ListView):
    context_object_name = "posts"
    template_name = 'blog/post_list.html'
    paginate_by = 4

    def get_queryset(self):
        posts = Post.objects.filter(status="pub", published_date__lte=timezone.now()).order_by('id')
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

    def get(self, request, *args, **kwargs):
        post = self.get_object()
        post.increment_counted_views()
        return super().get(request, *args, **kwargs)

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ('image', 'title', 'content', 'published_date', 'category')
    template_name = 'blog/post_update_create.html'
    success_url = reverse_lazy("blog:post_list")

    def form_valid(self, form):
        profile = get_object_or_404(Profile, user=self.request.user)
        form.instance.author = profile
        messages.success(self.request, "Post created Successfully and will be published after admin confirmation")
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, "Something is wrong")
        return self.render_to_response(self.get_context_data(form=form))
    

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ('image', 'title', 'content', 'published_date', 'category')
    template_name = 'blog/post_update_create.html'
    success_url = reverse_lazy("blog:post_list")

    def form_valid(self, form):
        profile = get_object_or_404(Profile, user=self.request.user)
        form.instance.author = profile
        form.instance.status = 'drf'
        messages.success(self.request, "Post updated successfully and will be published after admin confirmation")
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, "Something is wrong")
        return self.render_to_response(self.get_context_data(form=form))
    
    def test_func(self):
        profile = get_object_or_404(Profile, user=self.request.user)
        return self.get_object().author == profile

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'blog/post_delete.html'
    success_url = reverse_lazy('blog:post_list')

    def test_func(self):
        profile = get_object_or_404(Profile, user=self.request.user)
        return self.get_object().author == profile
    

class ManagePostListView(LoginRequiredMixin, ListView):
    context_object_name = 'posts'
    paginate_by = 4
    template_name = 'blog/post_management.html'

    def get_queryset(self):
        profile = get_object_or_404(Profile, user=self.request.user)
        return Post.objects.filter(author=profile).order_by('id')


