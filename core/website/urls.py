from django.urls import path
from django.views.generic.base import TemplateView
from . import views

app_name = 'website'

urlpatterns = [
    # Route to the homepage of the website
    path('', TemplateView.as_view(template_name='website/index.html'), name="home"),

    # Route to the about page
    path('about/', TemplateView.as_view(template_name='website/about.html'), name="about"),

    # Route to the contact page with a form for users to send messages
    path('contact/', views.ContactCreateView.as_view(), name="contact"),
]
