from django import forms

from .models import ContactMessage


class ContactForm(forms.ModelForm):
    """Formulario de contacto."""

    class Meta:
        model = ContactMessage
        fields = (
            'subject',
            'username',
            'email',
            'message',
            'is_register'
        )
