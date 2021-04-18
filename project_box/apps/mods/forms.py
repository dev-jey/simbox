from django import forms
from .models import Mod, Type


class ModCreateForm(forms.ModelForm):
    type_ = forms.ModelChoiceField(queryset=Type.objects.all().distinct())

    class Meta:
        model = Mod
        fields = ['title', 'type_', 'description', 'image', 'cover_image', 'mod_file']
        exclude = ('user',)

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super(ModCreateForm, self).__init__(*args, **kwargs)

    def clean_title(self):
        title = self.cleaned_data['title']
        if Mod.objects.filter(title=title).exists():
            raise forms.ValidationError("A mod with this title already exists.")
        return title
