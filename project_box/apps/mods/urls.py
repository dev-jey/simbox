"""
URL Configuration.

URL configurations for the terms application.
"""
from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from .views import (
    ModsDetailView,
    CreateModView,
    EditModView,
    DeleteModView,
    ModsListView
)

# Specify a namespace
app_name = "mods"

BASE_URL = 'mod'

urlpatterns = [
    # Mods link
    path(f'{BASE_URL}/<int:pk>/', ModsDetailView.as_view(), name='mod-detail'),
    path(f'{BASE_URL}/upload/', CreateModView.as_view(), name='create-mod'),
    path(f'{BASE_URL}/<int:pk>/update/', EditModView.as_view(), name='edit-mod'),
    path(f'{BASE_URL}/<int:pk>/delete/', DeleteModView.as_view(), name='delete-mod'),
    path(f'{BASE_URL}s/', ModsListView.as_view(), name='mods-list'),
]
