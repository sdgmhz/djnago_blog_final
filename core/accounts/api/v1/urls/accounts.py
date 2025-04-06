from django.urls import path
from rest_framework_simplejwt.views import (
    TokenRefreshView,
    TokenVerifyView
)


from .. import views
app_name = 'api-v1'

urlpatterns = [
    # Route to the user registration API, which handles sign-up with captcha validation
    path('registration/', views.RegistrationApiView.as_view(), name='registration'),

    # Route to auth token login endpoint (POST request required)
    path('token/login/', views.CustomObtainAuthToken.as_view(), name='token-login'),

    # Route to auth token logout endpoint (POST request required)
    path('token/logout/', views.CustomDiscardAuthToken.as_view(), name="token-logout"),

    # Route to obtain a new JWT token pair (access and refresh tokens)
    path('jwt/create/', views.CustomTokenObtainPairView.as_view(), name="jwt-create"),

    # Route to refresh an existing JWT token using a valid refresh token
    path('jwt/refresh/', TokenRefreshView.as_view(), name="jwt-refresh"),

    # Route to verify the validity of a given JWT token
    path('jwt/verify/', TokenVerifyView.as_view(), name="jwt-verify"),

    # Route to the change password API, which allows users to update their password
    path('change-password/', views.ChangePasswordApiView.as_view(), name='change-password'),

    # Route to confirm account activation with a token
    path('activation/confirm/<str:token>/', views.ActivationApiView.as_view(), name="activation"),

    # Route to resend activation email
    path('activation/resend/', views.ActivationResendApiView.as_view(), name="activation-resend"),

    # Route to request password reset by providing registered email
    path('password/reset/',views.PasswordResetApiView.as_view(), name='password-reset'),

    # Route to confirm password reset with the provided token
    path('password/reset/confirm/<str:token>/', views.PasswordResetConfirmApiView.as_view(), name="password-reset-confirm"),


]
