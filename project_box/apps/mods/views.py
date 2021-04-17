from django.http.response import Http404
from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView
from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from project_box.apps.mods.forms import ModCreateForm
from django.views.generic.base import TemplateView
from project_box.apps.mods.models import Mod


class ModDetailView(TemplateView):
    template_name = 'components/mods/singlemod.html'

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


class AddModView(LoginRequiredMixin, CreateView):
    template_name = 'components/mods/newmod.html'
    success_url = reverse_lazy('mods:mods-list')
    form_class = ModCreateForm
    success_message = "Mod created successfully"

    def form_valid(self, form):
        form.instance.created_by_user = self.request.user
        title = form.cleaned_data.get('title')
        description = form.cleaned_data.get('description')
        mod_file = form.cleaned_data.get('mod_file')
        image = form.cleaned_data.get('image')
        cover_image = form.cleaned_data.get('cover_image')
        import pdb
        pdb.set_trace()
        mod_file_size = 4.56
        obj = Mod.objects.create(
            title=title,
            description=description,
            mod_file_size=mod_file_size,
            mod_file=mod_file,
            image=image,
            cover_image=cover_image
        )
        obj.save()
        return super(ModCreateForm, self).form_valid(form)


class ModsListView(TemplateView):
    template_name = 'components/mods/allmods.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        return context


class CategoryView(TemplateView):
    template_name = 'components/mods/category.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        return context
