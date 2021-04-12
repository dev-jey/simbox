"""
URL Configuration.

URL configurations for the terms application.
"""
from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from .views import (
    HomeAPIView,
    VerifyAPIView,
    SignUpView
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
        LoginView.as_view(template_name='components/user/login.html'),
        name='login'),
    path(
        'signup/',
        SignUpView.as_view(),
        name='signup'),
    path('verify/<token>/',
         VerifyAPIView.as_view(),
         name='verify_email'),
    path('logout/',
         LogoutView.as_view(),
         name='logout'),
]
