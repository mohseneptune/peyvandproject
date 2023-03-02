from django.urls import path
from django.views.generic import RedirectView
from .views import home_view, contact_view, about_view



app_name = 'main'

urlpatterns = [
    path('', RedirectView.as_view(pattern_name='main:home')),
    path('home/', home_view, name='home'),
    path('contact/', contact_view, name='contact'),
    path('about/', about_view, name='about'),
]