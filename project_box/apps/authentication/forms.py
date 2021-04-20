from django import forms
from .models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput, help_text='Minimum 8 characters.')
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput, help_text='')
    agree_to_terms_and_conditions = forms.BooleanField(required = True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2','agree_to_terms_and_conditions']
        help_texts = {k: "" for k in fields}


class LoginForm(AuthenticationForm):

    username = forms.EmailField(required=True) 
    remember_me = forms.BooleanField(required = False)
    def __init__(self, *args, **kwargs):
        self.error_messages['invalid_login'] = 'Login failed. Username and password do not match.'
        super().__init__(*args, **kwargs)

    class Meta:
        model = User
        fields = ['username', 'password']


class UserUpdateForm(PasswordChangeForm):
    class Meta:
        model = User
        fields = ['email']
