from django import forms

from .models import QuickResource, Resource


class ResourceCreateForm(forms.ModelForm):
    """Form creación de un resource."""

    class Meta:
        model = Resource
        fields = (
            'owner',
            'title',
            'categories',
            'main_tag',
            'tags',
            'languages',
            'resource_format',
            'link',
            'require_register',
            'image',
            'description',
        )
        labels = {
            'require_register': '¿Requiere registro?',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['owner'].widget = forms.HiddenInput()


class QuickResourceCreateForm(forms.ModelForm):
    """Form creación de un recurso temporal."""

    class Meta:
        model = QuickResource
        fields = ('owner', 'title', 'link', 'message')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['owner'].widget = forms.HiddenInput()

    def clean_title(self):
        """Comprueba que no exista el titulo tambien en Resource."""
        title = self.cleaned_data['title']
        if Resource.objects.filter(title=title):
            msg_error = 'El titulo ya existe'
            raise forms.ValidationError(msg_error)
        return title
