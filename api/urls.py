from django.urls import path
from . import views


urlpatterns = [
    path('mod/', views.ModListView.as_view(), name="mod-search"),
]
