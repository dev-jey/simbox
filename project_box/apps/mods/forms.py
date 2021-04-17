from django import forms
from .models import Mod


class ModCreateForm(forms.ModelForm):
    title = forms.CharField(required=True, label='Mod Name')
    description = forms.CharField(required=True, label='Description')
    image = forms.ImageField(required=True, label='Image')
    cover_image = forms.ImageField(required=True, label='Cover Image')
    mod_file = forms.FileField(required=True)

    class Meta:
        model = Mod
        fields = ['title', 'description','image','cover_image', 'mod_file']
