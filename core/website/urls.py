from django.urls import path
from django.views.generic.base import TemplateView
from . import views

app_name = 'website'

urlpatterns = [
    path('', TemplateView.as_view(template_name = 'website/index.html'), name="home"),
    path('about/', TemplateView.as_view(template_name = 'website/about.html'), name="about"),
    path('contact/', views.ContactCreateView.as_view(), name="contact"),
]