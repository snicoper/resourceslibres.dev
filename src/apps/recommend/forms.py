from django import forms
from django.utils.translation import ugettext_lazy as _


class RecommendResourceForm(forms.Form):
    """Form para recomendar un resource por email."""
    from_email = forms.EmailField(
        label=_('Tu email')
    )
    recipient_email = forms.EmailField(
        label=_('Email destinatario')
    )
    message = forms.CharField(
        widget=forms.Textarea(),
        required=False,
        label=_('Mensaje')
    )
