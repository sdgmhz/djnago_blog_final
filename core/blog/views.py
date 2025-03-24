from django.shortcuts import get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic.edit import FormMixin
from django.utils import timezone
from django.urls import reverse_lazy
from django.contrib import messages

from .models import Post, Category
from accounts.models import Profile
from .forms import CategoryForm
from comment.models import Comment
from comment.forms import CommentForm


class PostListView(ListView):
    """ Displays a list of posts with filtering by category and author """
    context_object_name = "posts"
    template_name = 'blog/post_list.html'
    paginate_by = 4

    def get_queryset(self):
        """ Filters posts based on status, published date, category, and author email """
        posts = Post.objects.filter(status="pub", published_date__lte=timezone.now()).order_by('id')
        cat_name = self.kwargs.get('cat_name')
        author_email = self.kwargs.get('author_email')
        if cat_name:
            posts = posts.filter(category__name=cat_name)
        if author_email:
            posts = posts.filter(author__user__email=author_email)
        return posts

class PostDetailView(DetailView, FormMixin):
    """ Displays a single post and allows commenting """
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'
    queryset = Post.objects.filter(status='pub', published_date__lte=timezone.now())
    form_class = CommentForm

    def get(self, request, *args, **kwargs):
        """ Increments view count for the post before rendering it """
        post = self.get_object()
        post.increment_counted_views()
        return super().get(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        """ Adds comments and form to the context data """
        context = super().get_context_data(**kwargs)
        context['comments'] = Comment.objects.filter(post=self.object, approved=True)
        context["form"] = self.get_form()
        return context

    def post(self, request, *args, **kwargs):
        """ Handles form submission for posting comments """
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = self.object
            comment.save()
            messages.success(self.request, "Comment submitted successfully and will be published after admin confirmation")
            return redirect(self.request.path)
        messages.error(self.request, "Something is wrong")
        return self.get(request, *args, **kwargs)



class PostCreateView(LoginRequiredMixin, CreateView):
    """ Allows logged-in users to create a new post """
    model = Post
    fields = ('image', 'title', 'content', 'published_date', 'category')
    template_name = 'blog/post_update_create.html'
    success_url = reverse_lazy("blog:post_list")

    def form_valid(self, form):
        """ Assigns the logged-in user as the author of the post """
        profile = get_object_or_404(Profile, user=self.request.user)
        form.instance.author = profile
        messages.success(self.request, "Post created Successfully and will be published after admin confirmation")
        return super().form_valid(form)
    
    def form_invalid(self, form):
        """ Displays an error message if the form is invalid """
        messages.error(self.request, "Something is wrong")
        return self.render_to_response(self.get_context_data(form=form))
    
    def get_context_data(self, **kwargs):
        """ Adds categories to the context data for the form """
        context = super().get_context_data(**kwargs)
        context["categories"] = Category.objects.all()
        return context
    

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """ Allows logged-in users to update their own posts """
    model = Post
    fields = ('image', 'title', 'content', 'published_date', 'category')
    template_name = 'blog/post_update_create.html'
    success_url = reverse_lazy("blog:post_list")


    def form_valid(self, form):
        """ Sets the author and status of the post before saving """
        profile = get_object_or_404(Profile, user=self.request.user)
        form.instance.author = profile
        form.instance.status = 'drf'
        messages.success(self.request, "Post updated successfully and will be published after admin confirmation")
        return super().form_valid(form)
    
    def form_invalid(self, form):
        """ Displays an error message if the form is invalid """
        messages.error(self.request, "Something is wrong")
        return self.render_to_response(self.get_context_data(form=form))
    
    def test_func(self):
        """ Ensures that only the author of the post can update it """
        profile = get_object_or_404(Profile, user=self.request.user)
        return self.get_object().author == profile

    def get_context_data(self, **kwargs):
        """ Adds categories to the context data for the form """
        context = super().get_context_data(**kwargs)
        context["categories"] = Category.objects.all()
        return context

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """ Allows the author to delete their own post """
    model = Post
    template_name = 'blog/post_delete.html'
    success_url = reverse_lazy('blog:post_list')

    def test_func(self):
        """ Ensures that only the author of the post can delete it """
        profile = get_object_or_404(Profile, user=self.request.user)
        return self.get_object().author == profile
    

class ManagePostListView(LoginRequiredMixin, ListView):
    """ Displays a list of posts created by the logged-in user """
    context_object_name = 'posts'
    paginate_by = 4
    template_name = 'blog/post_management.html'

    def get_queryset(self):
        """ Filters posts by the logged-in user """
        profile = get_object_or_404(Profile, user=self.request.user)
        return Post.objects.filter(author=profile).order_by('id')
    

class CategoryListCreateView(LoginRequiredMixin, ListView, FormView):
    """ Displays categories and allows creating new categories """
    model = Category
    form_class = CategoryForm
    template_name = 'blog/category_list.html'
    context_object_name = 'categories'
    success_url = reverse_lazy("blog:category_list")

    def form_valid(self, form):
        """ Saves the new category to the database """
        form.save()
        return super().form_valid(form)
    


