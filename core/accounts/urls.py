from django.urls import path,include, reverse_lazy
from . import views
from django.contrib.auth.views import LoginView, PasswordChangeView, PasswordResetView, PasswordResetConfirmView

from .forms import CustomAuthenticationForm, CustomPasswordChangeForm, CustomPasswordResetForm, CustomSetPasswordForm

app_name = "accounts"

urlpatterns = [
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path("login/", LoginView.as_view(form_class=CustomAuthenticationForm), name='login'),
    path(
        "password_change/", PasswordChangeView.as_view(form_class=CustomPasswordChangeForm, success_url=reverse_lazy("accounts:password_change_done")), name="password_change"
    ),
    path("password_reset/", PasswordResetView.as_view(form_class=CustomPasswordResetForm, success_url=reverse_lazy("accounts:password_reset_done")), name="password_reset"),
    path(
        "reset/<uidb64>/<token>/",
        PasswordResetConfirmView.as_view(form_class=CustomSetPasswordForm,success_url=reverse_lazy("accounts:password_reset_complete")),
        name="password_reset_confirm",
    ),
    path('', include('django.contrib.auth.urls')),

]