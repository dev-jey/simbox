from django import forms
from .models import Mod, Type


class ModCreateForm(forms.ModelForm):
    simulator_ = forms.ModelChoiceField(queryset=Type.objects.all().distinct())
    screenshots = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple':
                                                                   True}))
    agree_to_terms_and_conditions = forms.BooleanField(required=True)

    class Meta:
        model = Mod
        fields = ['title', 'simulator_', 'description',  'header_image', 'cover_image','screenshots', 'mod_file']
        exclude = ('user',)

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super(ModCreateForm, self).__init__(*args, **kwargs)

    def clean_title(self):
        title = self.cleaned_data['title']
        if Mod.objects.filter(title=title).exists():
            raise forms.ValidationError("A mod with this title already exists.")
        return title
