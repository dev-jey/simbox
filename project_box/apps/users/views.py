import os
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin  # UserPassesTestMixin

from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.contrib import messages
from django.urls.base import reverse
from django.views.generic import DetailView, ListView, UpdateView
from django.views.generic.base import TemplateView
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from django.core.mail import send_mail

from project_box.apps.mods.models import Mod, ModsListConnector, ModsListName, ModsLike


class HomeAPIView(TemplateView):
    model = User
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['user'] = self.request.user
        return context


def register(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            form = UserRegisterForm(request.POST)
            if form.is_valid():
                form.save()
                username = form.cleaned_data.get('username')
                send_mail('Simbox Email Verification', 'Your account was successfully created. \
                    Kindlylick on the link below to verify your account.', os.getenv(
                    'EMAIL_HOST_USER'), [os.getenv('EMAIL_HOST_USER')])
                messages.success(request, f'Account created for {username}! Please verify your email to continue')
                return render(request, 'components/user/register.html', {'form': form})
        else:
            form = UserRegisterForm()
        return render(request, 'components/user/register.html', {'form': form})
    else:
        messages.success(request, 'Account created successfully. Welcome!')
        return redirect('/profile/' + request.user.username)


class ProfileView(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'users/profile.html'

    # Set header tags
    title = 'Profile - <username>'
    description = 'Simbox profile of <username>'
    og_image = '<profile><image><url>'

    def get_object(self):
        return get_object_or_404(User, username=self.kwargs.get('username'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['list_names'] = ModsListName.objects.filter(
            list_owner=User.objects.get(id=self.get_object().id)
        )

        context['likes'] = ModsLike.objects.filter(
            user_id=User.objects.get(id=self.get_object().id)
        )

        return context


class ProfileModsView(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'users/profile_mods.html'

    def get_object(self):
        return get_object_or_404(User, username=self.kwargs.get('username'))

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return User.objects.get(username=user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['mods'] = Mod.objects.filter(
            author=User.objects.get(pk=self.get_object().id)
        )

        return context


class ProfileListsView(LoginRequiredMixin, ListView):
    model = ModsListConnector
    template_name = 'users/profile_list_detail.html'

    def get_queryset(self):
        return ModsListConnector.objects.filter(
            list_id=self.kwargs.get('id')
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['object'] = User.objects.get(
            username=self.kwargs.get('username')
        )

        return context


class ProfileUpdate(LoginRequiredMixin, UpdateView):
    model = User
    template_name = 'users/update_profile.html'

    def get(self, request):
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

        context = {'u_form': u_form, 'p_form': p_form}
        return render(request, 'users/update_profile.html', context)

    def post(self, request, *args, **kwargs):
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(
            request.POST,
            request.FILES,
            instance=request.user.profile
        )
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()

            messages.success(request, 'Your account has been updated!')
            return redirect('/profile/' + request.user.username)


class ProfileUpdatePassword(PasswordChangeView):
    form_class = PasswordChangeForm
    template_name = 'users/update_profile.html'

    def get_success_url(self) -> str:
        messages.success(self.request, 'Password updated successfully.')
        return reverse_lazy('profile', kwargs={'username': self.request.user})
