"""
URL Configuration.

URL configurations for the terms application.
"""
from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from .views import (
    HomeAPIView,
    register
)

# Specify a namespace
app_name = "users"


urlpatterns = [
    path(
        '',
        HomeAPIView.as_view(),
        name='index'),

    path(
        'login/',
        LoginView.as_view(template_name='components/user/login.html'), name='login'),
    path(
        'signup/', register, name='signup'),
    path('logout/', LogoutView.as_view(), name='logout'),
]
