from django.urls import path
from django.views.generic.base import TemplateView

app_name = 'website'

urlpatterns = [
    path('', TemplateView.as_view(template_name = 'website/index.html'), name="home"),
    path('about/', TemplateView.as_view(template_name = 'website/about.html'), name="about"),
]