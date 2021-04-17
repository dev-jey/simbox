import os
from django.template.loader import render_to_string
from django.core.mail import send_mail
import jwt
from .models import User
from django.conf import settings
from django.contrib.sites.models import Site
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.forms import PasswordChangeForm
from .models import User
from django.contrib.auth.mixins import LoginRequiredMixin  # UserPassesTestMixin

from datetime import datetime, timedelta
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.contrib import messages
from django.urls.base import reverse
from django.views.generic import DetailView, ListView, UpdateView
from django.views.generic.base import TemplateView
from .forms import UserRegisterForm, UserUpdateForm
from project_box.apps.mods.models import Mod
from .forms import UserRegisterForm
from django.views.generic.edit import CreateView


class SignUpView(CreateView):
    template_name = 'components/user/register.html'
    success_url = reverse_lazy('authentication:login')
    form_class = UserRegisterForm
    success_message = "Your profile was created successfully"

    def send_email_activation_link(self, username, email, url):
        payload = {
            'email': email,
            'username': username,
            'exp': datetime.utcnow() + timedelta(minutes=60)
        }
        token = jwt.encode(payload, settings.SECRET_KEY,
                           algorithm='HS256')
        sender = os.getenv('EMAIL_HOST_USER')
        link = f"http://{url}/verify/{token}"
        email_subject = "Simbox Email verification"
        message = render_to_string('components/user/email/verification_template.html', {
            'title': email_subject,
            'username': username,
            'verification_link': link
        })
        send_mail(email_subject, '', sender, [email, ], html_message=message)

    def form_valid(self, form):
        form.instance.created_by_user = self.request.user
        username = form.cleaned_data.get('username')
        email = form.cleaned_data.get('email')
        url = Site.objects.get_current().domain
        self.send_email_activation_link(username, email, url)
        return super(SignUpView, self).form_valid(form)


class HomeAPIView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['user'] = self.request.user
        return context


class VerifyAPIView(TemplateView):
    template_name = 'verify.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        token = self.kwargs['token']
        try:
            token_decode = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            email = token_decode['email']
            user = User.objects.get(email=email)
            username = token_decode['username']
            if user.is_verified:
                message = 'Account already activated. Click on the link to continue'
            user.is_verified = True
            user.save()
            message = f'Welcome {username}, \nYour email has been successfully activated.'
        except Exception as e:
            print(e)
            message = 'Verification token is not valid. Try again'
        context['user'] = self.request.user
        context['message'] = message
        return context


class ProfileAPIView(LoginRequiredMixin, TemplateView):
    template_name = 'profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['user'] = self.request.user
        return context


class ProfileModsAPIView(TemplateView):
    template_name = 'usermods.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['user'] = self.request.user
        return context
