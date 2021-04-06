from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import News


class NewsListView(LoginRequiredMixin, ListView):
    model = News
    ordering = ['-datetime_created']
