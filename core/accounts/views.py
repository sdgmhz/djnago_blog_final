from django.shortcuts import get_object_or_404
from django.views import generic
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages

from .forms import CustomUserCreationForm
from .models import Profile


class SignUpView(generic.CreateView):
    form_class = CustomUserCreationForm
    template_name = 'registration/signup.html'
    success_url = reverse_lazy('home')


class UpdateProfileView(LoginRequiredMixin, generic.UpdateView):
    model = Profile
    fields = ('first_name', 'last_name', 'image', 'description')
    template_name = 'registration/profile.html'

    def get_success_url(self):
        return reverse_lazy('accounts:update_profile')
    
    def form_valid(self, form):
        messages.success(self.request, "Profile Updated successfully")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Something is wrong")
        return self.render_to_response(self.get_context_data(form=form))
    
    def get_object(self, queryset=None):
        return get_object_or_404(Profile, user=self.request.user)

