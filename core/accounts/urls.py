from django.urls import path,include
from . import views
from django.contrib.auth.views import LoginView

from .forms import CustomAuthenticationForm

app_name = "accounts"

urlpatterns = [
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path("login/", LoginView.as_view(form_class=CustomAuthenticationForm), name='login'),
    path('', include('django.contrib.auth.urls')),

]