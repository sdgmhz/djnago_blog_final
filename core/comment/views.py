from django.shortcuts import get_object_or_404
from django.views.generic import ListView, DetailView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.contrib import messages

from .models import Comment
from accounts.models import Profile

class CommentListView(LoginRequiredMixin, ListView):
    context_object_name = 'comments'
    template_name = 'comment/comment_list.html'
    paginate_by = 6

    def get_queryset(self):
        profile = get_object_or_404(Profile, user=self.request.user)
        return Comment.objects.filter(email=profile, created_date__gt=profile.created_date)
    
class CommentDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Comment
    context_object_name = 'comment'
    template_name = 'comment/comment_detail.html'

    def test_func(self):
        profile = get_object_or_404(Profile, user=self.request.user)
        return self.get_object().email == str(profile) and self.get_object().created_date > profile.created_date
class CommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Comment
    fields = ('name', 'subject', 'message', 'recommend', )
    template_name = 'comment/comment_update.html'
    success_url = reverse_lazy("comment:comment_list")

    def form_valid(self, form):
        profile = get_object_or_404(Profile, user=self.request.user)
        post = self.get_object().post
        form.instance.email = str(profile)
        form.instance.approved = False
        form.instance.post = post
        messages.success(self.request, "Comment updated successfully and will be published after admin confirmation")
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, "Something is wrong")
        return self.render_to_response(self.get_context_data(form=form))
    
    def test_func(self):
        profile = get_object_or_404(Profile, user=self.request.user)
        return self.get_object().email == str(profile) and self.get_object().created_date > profile.created_date

class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment
    template_name = 'comment/comment_delete.html'    
    success_url = reverse_lazy("comment:comment_list")

    def test_func(self):
        profile = get_object_or_404(Profile, user=self.request.user)
        return self.get_object().email == str(profile) and self.get_object().created_date > profile.created_date

