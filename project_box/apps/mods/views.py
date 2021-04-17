import os
from django.http.response import Http404, HttpResponseRedirect
from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView
from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from project_box.apps.mods.forms import ModCreateForm
from django.views.generic.base import TemplateView
from project_box.apps.mods.models import Mod
from django.contrib import messages
from io import BytesIO

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


class AddModView(LoginRequiredMixin, CreateView):
    template_name = 'components/mods/newmod.html'
    success_url = reverse_lazy('mods:mods-list')
    form_class = ModCreateForm
    success_message = "Mod created successfully"

    def get_form_kwargs(self, *args, **kwargs):
        kwargs = super(AddModView, self).get_form_kwargs(*args, **kwargs)
        kwargs['user'] = self.request.user
        return kwargs

    # def form_valid(self, form):
    #     title = form.cleaned_data.get('title')
    #     description = form.cleaned_data.get('description')
    #     mod_file = self.request.FILES['mod_file']
    #     image = self.request.FILES['image']
    #     cover_image = self.request.FILES['cover_image']
    #     # Upload items to aws, store in well organized folders
    #     self.validate_and_upload_files(image, self.request.user, 'image')
    #     self.validate_and_upload_files(cover_image, self.request.user, 'image')
    #     self.validate_and_upload_files(mod_file, self.request.user)
    #     # Mod.objects.create(
    #     #     title=title,
    #     #     description=description
    #     # )
    #     return super(AddModView, self).form_valid(form)

    def validate_and_upload_files(self, file_obj, user, image=None):

        # organize a path for the file in bucket
        if image:
            file_directory_within_bucket = 'user_mod_image_files/{username}'.format(username=user)
        else:
            file_directory_within_bucket = 'user_mod_files/{username}'.format(username=user)

        # synthesize a full file path; note that we included the filename
        file_path_within_bucket = os.path.join(
            file_directory_within_bucket,
            file_obj.name
        )
        media_storage = MediaStorage()
        media_storage.save(file_path_within_bucket, file_obj)
        # file_url = media_storage.url(file_path_within_bucket)

        # if not media_storage.exists(file_path_within_bucket):  # avoid overwriting existing file
        #     media_storage.save(file_path_within_bucket, file_obj)

        #     return JsonResponse({
        #         'message': 'OK',
        #         'fileUrl': file_url,
        #     })
        # else:
        #     return JsonResponse({
        #         'message': 'Error: file {filename} already exists at {file_directory} in bucket {bucket_name}'.format(
        #             filename=file_obj.name,
        #             file_directory=file_directory_within_bucket,
        #             bucket_name=media_storage.bucket_name
        #         ),
        #     }, status=400)


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
        context['user'] = self.request.user
        return context


class CategoryView(TemplateView):
    template_name = 'components/mods/category.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        return context
