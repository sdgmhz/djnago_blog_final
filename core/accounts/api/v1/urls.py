from django.urls import path


from . import views
app_name = 'api-v1'

urlpatterns = [
    # Route to the user registration API, which handles sign-up with captcha validation
    path('registration/', views.RegistrationApiView.as_view(), name='registration'),

    # Route to auth token login endpoint (POST request required)
    path('token/login/', views.CustomObtainAuthToken.as_view(), name='token-login'),

    # Route to auth token logout endpoint (POST request required)
    path('token/logout/', views.CustomDiscardAuthToken.as_view(), name="token-logout"),


]
