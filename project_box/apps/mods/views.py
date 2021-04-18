import os
from project_box.apps.mods.resize_mixin import ResizeImageMixin
from django.http.response import Http404, HttpResponseRedirect
from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView
from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from project_box.apps.mods.forms import ModCreateForm
from django.views.generic.base import TemplateView
from project_box.apps.mods.models import Mod, Type
from django.contrib import messages
from io import BytesIO
import uuid

from django.http import JsonResponse

from project_box.storage_backends import MediaStorage


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


class AddModView(LoginRequiredMixin, CreateView, ResizeImageMixin):
    template_name = 'components/mods/newmod.html'
    success_url = reverse_lazy('mods:mods-list')
    form_class = ModCreateForm
    success_message = "Mod created successfully"

    def get_form_kwargs(self, *args, **kwargs):
        kwargs = super(AddModView, self).get_form_kwargs(*args, **kwargs)
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        self.mod_file = self.request.FILES['mod_file']
        self.image = self.request.FILES['image']
        self.cover_image = self.request.FILES['cover_image']
        # Upload items to aws, store in well organized folders
        self.compressed_image = self.resize(self.image, (400, 400))
        image_url = self.validate_and_upload_files(self.compressed_image, self.request.user, 'image')
        self.compressed_cover_image = self.resize(self.cover_image, (400, 400))
        cover_image_url = self.validate_and_upload_files(self.compressed_cover_image, self.request.user, 'image')
        mod_file_url = self.validate_and_upload_files(self.mod_file, self.request.user)
        self.object = form.save(commit=False)
        self.object.image = image_url
        self.object.cover_image = cover_image_url
        self.object.mod_file = mod_file_url
        self.object.save()
        form.cleaned_data['type_'].mods.add(self.object)
        self.request.user.mods.add(self.object)
        return HttpResponseRedirect(self.get_success_url())

    def validate_and_upload_files(self, file_obj, user, image=None):
        # organize a path for the file in bucket
        if image:
            file_directory_within_bucket = 'user_mod_image_files/{username}'.format(username=user)
        else:
            file_directory_within_bucket = 'user_mod_files/{username}'.format(username=user)
        # synthesize a full file path; note that we included the filename
        file_path_within_bucket = os.path.join(
            file_directory_within_bucket,
            f'{uuid.uuid4()}.jpg'
        )
        media_storage = MediaStorage()
        # file_url = media_storage.url(file_path_within_bucket)
        return media_storage.save(file_path_within_bucket, file_obj)


class EditModView(LoginRequiredMixin, CreateView):
    template_name = 'components/mods/newmod.html'
    success_url = reverse_lazy('mods:mods-list')
    form_class = ModCreateForm
    success_message = "Mod created successfully"

    def get_initial(self, *args, **kwargs):
        initial = super(EditModView, self).get_initial(**kwargs)
        initial['title'] = 'My Title'
        return initial

    def form_valid(self, form):
        form.instance.created_by_user = self.request.user
        title = form.cleaned_data.get('title')
        description = form.cleaned_data.get('description')
        obj = Mod.objects.update(
            title=title,
            description=description,
        )
        obj.save()
        return super(EditModView, self).form_valid(form)


class ModsListView(TemplateView):
    template_name = 'components/mods/allmods.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        mods = Mod.objects.all().order_by('-title')
        types = Type.objects.all()
        msfs = types.filter(name='MSFS').first()
        p3d = types.filter(name='P3D').first()
        x_plane = types.filter(name='X-PLANE').first()
        context['user'] = self.request.user
        context['mods'] = mods[:10]
        context['msfs_mods'] = msfs.mods.all()[:10]
        context['p3d_mods'] = p3d.mods.all()[:10]
        context['msfs'] = msfs
        context['x_plane'] = x_plane
        context['p3d'] = p3d
        context['x_plane_mods'] = x_plane.mods.all()[:10]
        return context


class CategoryView(TemplateView):
    template_name = 'components/mods/category.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = Type.objects.filter(id=self.kwargs['pk']).first()
        category_mods = category.mods.all()
        top_category_mods = category_mods[:10]
        context['user'] = self.request.user
        context['category'] = category
        context['category_mods'] = category_mods
        context['top_category_mods'] = top_category_mods

        return context
