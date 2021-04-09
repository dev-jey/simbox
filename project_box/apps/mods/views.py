from django.http.response import Http404
from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView
from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.db import transaction
from django.views.generic.base import TemplateView



from .models import (
    Mod,
)


class ModDetailView(TemplateView):
    model = Mod
    template_name = 'mods/mod_details.html'

    title = '<title>'
    description = 'Download <title> now for your flight simulator!'
    og_image = '<image><url>'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        return context

    def get_client_ip(self):
        '''Get client IP address to allow for unique views on each mod.'''
        x_forwarded_for = self.request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = self.request.META.get('REMOTE_ADDR')
        return ip


class ModsListView(ListView):
    model = Mod
