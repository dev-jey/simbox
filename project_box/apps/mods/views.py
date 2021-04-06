from django.http.response import Http404
from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView
from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.db import transaction

from project_box.apps.mixins.template import HeaderMixin

from .forms import (
    AddModToListForm,
    CreateNewListForm,
    CreateCommentForm,
    ModCreateForm,
    ModFormSet
)

from .models import (
    Mod,
    ModsLike,
    ModsView,
    ModsGallery,
    ModsListName,
    ModsListConnector,
    ModComments,
    ModsDownloadsCounter
)


class ModsDetailView(LoginRequiredMixin, HeaderMixin, DetailView):
    model = Mod

    title = '<title>'
    description = 'Download <title> now for your flight simulator!'
    og_image = '<image><url>'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        mod_instance = self.get_object()

        context['screenshots'] = ModsGallery.objects.filter(
            mod=self.kwargs['pk']
        )[:5]

        context['like_count'] = ModsLike.objects.filter(
            mod_id=mod_instance
        ).count()

        context['view_count'] = ModsView.objects.filter(
            mod_id=mod_instance
        ).count()

        context['downloads'] = ModsDownloadsCounter.objects.filter(
            mod_id=mod_instance
        ).count()

        context['comments'] = ModComments.objects.filter(
            mod_id=mod_instance
        )

        if self.request.user.is_authenticated:
            # Add context data
            context['has_liked'] = ModsLike.objects.filter(
                mod_id=self.kwargs['pk'],
                user_id=self.request.user
            )

            context['lists'] = ModsListName.objects.filter(
                list_owner=self.request.user
            )

            # Populate dropdown with mod lists from user
            add_to_list_form = AddModToListForm()
            add_to_list_form.fields['list_name'].queryset = ModsListName.objects.filter(list_owner=self.request.user)
            context['add_to_list_form'] = add_to_list_form

            context['create_new_list_form'] = CreateNewListForm()
            context['create_comment_form'] = CreateCommentForm()

        # Save view as new if not already existent
        ip = self.get_client_ip()
        ModsView.objects.get_or_create(mod_id=mod_instance, IPAddress=ip)

        return context

    # Handle post requests (mainly Ajax)
    def post(self, request, *args, **kwargs):
        mod = self.get_object()
        user = request.user
        ajax_data = request.POST

        # Create a list for mods
        if (ajax_data.get('action') == 'create-list'):
            new_list_form = CreateNewListForm(request.POST)

            if new_list_form.is_valid():
                obj = ModsListName()
                obj.list_name = new_list_form.cleaned_data['list_name']
                obj.list_owner = user
                obj.save()

                return JsonResponse({'list_id': obj.id, 'list_name': obj.list_name}, status=200)

        # Add mod to list
        elif (ajax_data.get('action') == 'add-to-list'):
            add_to_list_form = AddModToListForm(request.POST)

            if add_to_list_form.is_valid():
                obj = ModsListConnector()
                obj.list_id = ModsListName.objects.filter(list_name=add_to_list_form.cleaned_data['list_name']).first()
                obj.mod_id = mod
                obj.user_id = user
                obj.save()

                return JsonResponse(
                    {'message': f'{mod.title} has been added to list "{obj.list_id.list_name}"'}, status=200)

        # Add or delete like
        elif (ajax_data.get('action') == 'like'):
            # Save new like if it doesn't exist. If it exists, delete it.
            if(ModsLike.objects.filter(mod_id=mod, user_id=user).exists()):
                ModsLike.objects.get(mod_id=mod, user_id=user).delete()
                return JsonResponse({'message': 'Removed like.'}, status=200)
            else:
                ModsLike(mod_id=mod, user_id=user).save()
                return JsonResponse({'message': 'Thank you for your like!'}, status=200)

        # Save comment
        elif (ajax_data.get('action') == 'save-comment'):
            create_comment_form = CreateCommentForm(request.POST)

            if create_comment_form.is_valid():
                obj = ModComments()
                obj.text = create_comment_form.cleaned_data['text']
                obj.user_id = user
                obj.mod_id = mod
                obj.save()

                return JsonResponse({'message': 'Comment has been saved.'}, status=200)

        # Delete comment
        elif (ajax_data.get('action') == 'delete-comment'):
            comment = ModComments.objects.filter(id=ajax_data.get('comment')).first()

            if (user == comment.user_id):
                comment.delete()
                return JsonResponse({'message': 'Comment has been deleted.'}, status=200)
            else:
                return JsonResponse({"status", "Forbidden access."}, status=500)

        # Download counter
        elif (ajax_data.get('action') == 'download'):
            ip = self.get_client_ip()
            ModsDownloadsCounter.objects.get_or_create(
                mod_id=mod,
                IPAddress=ip
            )
            return JsonResponse({'message': 'Comment has been deleted.'}, status=200)

        else:
            Http404("Something went wrong during the request!")

    def get_client_ip(self):
        '''Get client IP address to allow for unique views on each mod.'''
        x_forwarded_for = self.request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = self.request.META.get('REMOTE_ADDR')
        return ip


class ModsListView(LoginRequiredMixin, ListView):
    model = Mod


class CreateModView(LoginRequiredMixin, CreateView):
    model = Mod
    form_class = ModCreateForm

    def get_context_data(self, **kwargs):
        context = super(CreateModView, self).get_context_data(**kwargs)

        if self.request.POST:
            context['images'] = ModFormSet(self.request.POST)
            context['images'].full_clean()
        else:
            context['images'] = ModFormSet()
        return context

    def form_valid(self, form):
        images_formset = ModFormSet(self.request.POST, self.request.FILES, instance=form.instance)

        form.instance.author = self.request.user

        with transaction.atomic():
            if images_formset.is_valid():
                response = super().form_valid(form)
                images_formset.mod = self.object
                images_formset.save()

                return response
            else:
                return super(EditModView, self).form_invalid(form)

    def get_success_url(self) -> str:
        return reverse_lazy('mod-detail', kwargs={'pk': self.object.pk})


class EditModView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Mod
    form_class = ModCreateForm

    def get_context_data(self, **kwargs):
        context = super(EditModView, self).get_context_data(**kwargs)

        if self.request.POST:
            context['images'] = ModFormSet(self.request.POST, instance=self.object)
            context['images'].full_clean()
        else:
            context['images'] = ModFormSet(instance=self.object)
        return context

    def form_valid(self, form):
        images_formset = ModFormSet(self.request.POST, self.request.FILES, instance=form.instance)

        form.instance.author = self.request.user

        with transaction.atomic():
            if images_formset.is_valid():
                images_formset.mod = self.object
                images_formset.save()

                response = super().form_valid(form)
                return response
            else:
                return super(EditModView, self).form_invalid(form)

    # Check if requesting user is the author of the mod
    def test_func(self):
        mod = self.get_object()
        return self.request.user == mod.author

    def get_success_url(self) -> str:
        return reverse_lazy('mod-detail', kwargs={'pk': self.object.pk})


class DeleteModView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Mod

    def test_func(self):
        mod = self.get_object()
        return self.request.user == mod.author

    def get_success_url(self) -> str:
        return reverse_lazy('profile', kwargs={'username': self.request.user})
