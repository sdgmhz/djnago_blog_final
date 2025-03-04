from django.urls import path,include, reverse_lazy
from . import views
from django.contrib.auth.views import LoginView, PasswordChangeView

from .forms import CustomAuthenticationForm, CustomPasswordChangeForm

app_name = "accounts"

urlpatterns = [
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path("login/", LoginView.as_view(form_class=CustomAuthenticationForm), name='login'),
    path(
        "password_change/", PasswordChangeView.as_view(form_class=CustomPasswordChangeForm, success_url = reverse_lazy("accounts:password_change_done")), name="password_change"
    ),
    path('', include('django.contrib.auth.urls')),

]