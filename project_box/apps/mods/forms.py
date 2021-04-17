from django import forms
from .models import Mod


class ModCreateForm(forms.ModelForm):
    class Meta:
        model = Mod
        fields = ['title', 'description', 'image', 'cover_image', 'mod_file']
        exclude = ('user',)

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super(ModCreateForm, self).__init__(*args, **kwargs)

    def clean_title(self):
        title = self.cleaned_data['title']
        if Mod.objects.filter(title=title).exists():
            raise forms.ValidationError("A mod with this title already exists.")
        return title
