import os
from django.template.loader import render_to_string
from django.core.mail import send_mail
import jwt
from .models import User
from django.conf import settings
from django.contrib.sites.models import Site
from django.contrib.auth.views import LoginView, PasswordChangeView
from .models import User
from django.contrib.auth.mixins import LoginRequiredMixin  # UserPassesTestMixin

from django.shortcuts import HttpResponseRedirect
from django.contrib.auth import login as auth_login
from datetime import datetime, timedelta
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.contrib import messages
from django.urls.base import reverse
from django.views.generic.base import TemplateView
from .forms import LoginForm, UserRegisterForm, UserUpdateForm
from project_box.apps.mods.models import Mod, Type
from .forms import UserRegisterForm
from django.views.generic.edit import CreateView
from django.contrib import messages


class UserUpdateView(PasswordChangeView):
    """
    Custom user update view.
    """
    template_name = 'profile.html'
    success_url = reverse_lazy('authentication:profile')
    form_class = UserUpdateForm
    success_message = "Profile Updated Successfully Successful"

class CustomLoginView(LoginView):
    """
    Custom login view.
    """
    template_name = 'components/user/login.html'
    success_url = reverse_lazy('authentication:home')
    form_class = LoginForm
    success_message = "Login Successful"

    def get_initial(self):
        if self.request.user.is_authenticated:
            return HttpResponseRedirect(reverse('{}'.format(self.request.GET.get('next', 'authentication:index'))))
        else:
            return self.initial.copy()

    def post(self, request, *args, **kwargs):
        """
        Handle POST requests: instantiate a form instance with the passed
        POST variables and then check if it's valid.
        """
        form = self.get_form()
        messages.error(self.request, '')
        if form.is_valid():
            user = form.get_user()
            if user.is_verified:
                auth_login(self.request, user)
                if not form.cleaned_data['remember_me']:
                    self.request.session.set_expiry(0)
                return self.form_valid(form)
            else:
                messages.error(
                    self.request, 'Kindly verify your account to login. Check your email for a verification link.')
                return self.form_invalid(form)
        else:
            return self.form_invalid(form)


class SignUpView(CreateView):
    template_name = 'components/user/register.html'
    success_url = reverse_lazy('authentication:login')
    form_class = UserRegisterForm
    success_message = "Your account was created successfully"

    def send_email_activation_link(self, username, email, url):
        payload = {
            'email': email,
            'username': username,
            'exp': datetime.utcnow() + timedelta(minutes=600000)
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
        messages.success(
            self.request, 'Your account has been created successfuly. We have sent an email verification link to your email. Kindly verify your email to login.')
        return super(SignUpView, self).form_valid(form)


class HomeAPIView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # categories = Type.objects.all()
        top_mods = Mod.objects.all()[:3]
        context['user'] = self.request.user
        context['top_mods'] = top_mods
        # context['categories'] = categories
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


class ProfileModsAPIView(TemplateView):
    template_name = 'usermods.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['user'] = User.objects.filter(username=kwargs['username']).first()
        return context
