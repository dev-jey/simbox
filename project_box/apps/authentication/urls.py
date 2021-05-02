"""
URL Configuration.

URL configurations for the terms application.
"""
from django.urls import path
from django.contrib.auth.views import LogoutView
from django.views.generic.base import TemplateView
from .views import (
    HomeAPIView,
    VerifyAPIView,
    SignUpView,
    UserUpdateView,
    ProfileModsAPIView,
    CustomLoginView,
    ContactView
)

# Specify a namespace
app_name = "authentication"


urlpatterns = [
    path(
        '',
        HomeAPIView.as_view(),
        name='index'),
    path(
        'login/',
        CustomLoginView.as_view(),
        name='login'),
    path(
        'signup/',
        SignUpView.as_view(),
        name='signup'),
    path('verify/<token>/',
         VerifyAPIView.as_view(),
         name='verify_email'),
    path('profile/',
         UserUpdateView.as_view(),
         name='profile'),
    path('profile/<username>/',
         ProfileModsAPIView.as_view(),
         name='profile-mods'),
    path('logout/',
         LogoutView.as_view(),
         name='logout'),
    path('guide/',
         TemplateView.as_view(template_name="components/extras/guide.html"),
         name='guide'),
    path('terms/',
         TemplateView.as_view(template_name="components/extras/terms.html"),
         name='terms'),
    path('contact/',
         ContactView.as_view(),
         name='contact'),
]
