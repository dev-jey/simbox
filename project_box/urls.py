"""project_box URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from project_box.apps.users import views as user_views
from project_box.apps.news.views import NewsListView
from project_box.apps.mods.views import (
    ModsDetailView,
    ModsListView,
    CreateModView,
    EditModView,
    DeleteModView,
)

import debug_toolbar


urlpatterns = [
    path('admin/', admin.site.urls),

    path('', include(('project_box.apps.users.urls',
                      'users'), namespace='users')),

    # Profile links
    path('profile/<str:username>/', user_views.ProfileView.as_view(), name='profile'),
    path('profile/<str:username>/mods/', user_views.ProfileModsView.as_view(), name='profile-mods'),
    path('profile/<str:username>/list/<int:pk>/', user_views.ProfileListsView.as_view(), name='profile-list-detail'),

    path('settings/', user_views.ProfileUpdate.as_view(), name='profile-update'),
    path('settings/security/', user_views.ProfileUpdatePassword.as_view(), name='profile-update-security'),

    # Mods link
    path('mod/<int:pk>/', ModsDetailView.as_view(), name='mod-detail'),
    path('mod/upload/', CreateModView.as_view(), name='create-mod'),
    path('mod/<int:pk>/update/', EditModView.as_view(), name='edit-mod'),
    path('mod/<int:pk>/delete/', DeleteModView.as_view(), name='delete-mod'),
    path('mods/', ModsListView.as_view(), name='mods-list'),

    # API
    path('api/', include('project_box.apps.api.urls')),

    # Misc
    path('tinymce/', include('tinymce.urls')),
    path('__debug__/', include(debug_toolbar.urls)),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
