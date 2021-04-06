from django import forms
from django.forms.models import inlineformset_factory
from .models import Mod, ModsListName, ModComments, ModsGallery, Simulator
from tinymce.widgets import TinyMCE


class AddModToListForm(forms.ModelForm):
    list_name = forms.ModelChoiceField(
        queryset=ModsListName.objects.all()
    )

    def __init__(self, *args, **kwargs):
        super(AddModToListForm, self).__init__(*args, **kwargs)

    class Meta:
        model = ModsListName
        fields = ['list_name']


class CreateNewListForm(forms.ModelForm):

    list_name = forms.CharField(widget=forms.TextInput, label='')

    def __init__(self, *args, **kwargs):
        super(CreateNewListForm, self).__init__(*args, **kwargs)
        self.fields['list_name'].widget.attrs['class'] = 'hidden'
        self.fields['list_name'].widget.attrs['id'] = 'new-list-name'

    class Meta:
        model = ModsListName
        fields = ['list_name']


class CreateCommentForm(forms.ModelForm):
    text = forms.CharField(
        widget=forms.Textarea(attrs={"cols": 29, "rows": 5}),
        label=''
    )

    class Meta:
        model = ModComments
        fields = ['text']


class ModCreateForm(forms.ModelForm):

    # Display a list of simulators as checkboxes
    simulators = forms.ModelMultipleChoiceField(
        queryset=Simulator.objects.all(),
        widget=forms.CheckboxSelectMultiple
    )

    class Meta:
        model = Mod
        exclude = ['author', 'mod_file_size']


class ModGalleryForm(forms.ModelForm):

    class Meta:
        model = ModsGallery
        exclude = ("image_thumb",)


ModFormSet = inlineformset_factory(
    Mod, ModsGallery,
    form=ModGalleryForm,
    extra=4
)
