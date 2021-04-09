"""
URL Configuration.

URL configurations for the terms application.
"""
from django.urls import path
from .views import (
    ModDetailView,
    # CreateModView,
    # EditModView,
    # DeleteModView,
    ModsListView
)

# Specify a namespace
app_name = "mods"

urlpatterns = [
    # Mods link
    path(f'<int:pk>/', ModDetailView.as_view(), name='mod-detail'),
    # path(f'upload/', CreateModView.as_view(), name='create-mod'),
    # path(f'<int:pk>/update/', EditModView.as_view(), name='edit-mod'),
    # path(f'<int:pk>/delete/', DeleteModView.as_view(), name='delete-mod'),
    path(f'', ModsListView.as_view(), name='mods-list'),
]
