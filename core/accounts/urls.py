from django.urls import path, include, reverse_lazy
from . import views
from django.contrib.auth.views import LoginView, PasswordChangeView, PasswordResetView, PasswordResetConfirmView

from .forms import CustomAuthenticationForm, CustomPasswordChangeForm, CustomPasswordResetForm, CustomSetPasswordForm

app_name = "accounts"

urlpatterns = [
    # Route to user signup view
    path('signup/', views.SignUpView.as_view(), name='signup'),

    # Route to user login view with custom authentication form
    path("login/", LoginView.as_view(form_class=CustomAuthenticationForm), name='login'),

    # Route to password change view with custom form and redirect after success
    path(
        "password_change/", PasswordChangeView.as_view(form_class=CustomPasswordChangeForm, success_url=reverse_lazy("accounts:password_change_done")), name="password_change"
    ),

    # Route to password reset view with custom form and redirect after success
    path("password_reset/", PasswordResetView.as_view(form_class=CustomPasswordResetForm,
         success_url=reverse_lazy("accounts:password_reset_done")), name="password_reset"),

    # Route to password reset confirm view with custom set password form and redirect after success
    path(
        "reset/<uidb64>/<token>/",
        PasswordResetConfirmView.as_view(form_class=CustomSetPasswordForm, success_url=reverse_lazy(
            "accounts:password_reset_complete")),
        name="password_reset_confirm",
    ),

    # Route to update profile view
    path('profile/update/', views.UpdateProfileView.as_view(), name="update_profile"),

    # Route to include default Django auth URLs
    path('', include('django.contrib.auth.urls')),

    # Include API URLs from the accounts's API version
    path('api/v1/', include('accounts.api.v1.urls')),

]
