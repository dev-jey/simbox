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

from project_box.apps.mods.models import Mod


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
