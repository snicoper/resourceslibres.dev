from django import forms
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.mixins import AccessMixin, PermissionRequiredMixin
from django.shortcuts import Http404
from django.urls import reverse
from django.views import generic

from utils.http import get_full_path
from utils.mail import send_templated_mail

from .forms import ContactForm
from .models import ContactMessage


class ContactView(generic.CreateView):
    """Muestra un formulario de contacto.

    Si es un usuario anónimo, mostrara el campo email,
    si es un usuario logueado, no mostrara el campo email.
    """
    template_name = 'contact/contact.html'
    form_class = ContactForm
    model = ContactMessage

    def get_form(self, form_class=None):
        """Si es un usuario logueado, obtener el email."""
        form = super().get_form(form_class)
        form.fields['is_register'].widget = forms.HiddenInput()
        form.initial['is_register'] = self.request.user.is_authenticated
        if self.request.user.is_authenticated:
            form.fields['username'].widget = forms.HiddenInput()
            form.initial['username'] = self.request.user.username
            form.fields['email'].widget = forms.HiddenInput()
            form.initial['email'] = self.request.user.email
        return form

    def form_valid(self, form):
        self._send_email_notification(form)
        return super().form_valid(form)

    def get_success_url(self):
        msg_success = 'Se ha enviado el mensaje a un administrador'
        messages.success(self.request, msg_success)
        return reverse('home_page')

    def _send_email_notification(self, form):
        """Envia un email de notificación."""
        subject = form.cleaned_data['subject']
        message = form.cleaned_data['message']
        user_email = form.cleaned_data['email']
        username = form.cleaned_data['username']
        is_register = form.cleaned_data['is_register']
        link_message = get_full_path(self.request, 'contact:list')
        context = {
            'register_text': 'registrado' if is_register else 'no registrado',
            'username': username,
            'user_email': user_email,
            'subject': subject,
            'message': message,
            'link_message': link_message
        }
        send_templated_mail(
            subject=subject,
            from_email=user_email,
            recipients=settings.GROUP_EMAILS['CONTACTS'],
            context=context,
            template_text='contact/emails/contact.txt',
            reply_to=[user_email]
        )


class BaseContactMessageMixin(PermissionRequiredMixin, AccessMixin):
    """Requiere permisos para ver los mensajes o lanzara 404."""
    model = ContactMessage
    permission_required = 'contact.can_view_messages'

    def handle_no_permission(self):
        raise Http404


class ContactMessageListView(BaseContactMessageMixin, generic.ListView):
    """Lista de mensajes."""
    template_name = 'contact/list.html'
    context_object_name = 'message_list'
    paginate_by = 10


class ContactMessageDetailView(BaseContactMessageMixin, generic.DetailView):
    """Detalles de un mensaje."""
    template_name = 'contact/details.html'
    context_object_name = 'message'

    def dispatch(self, request, *args, **kwargs):
        """Marca el mensaje como leído."""
        message = self.get_object()
        if not message.read:
            message.read = True
            message.save()
        return super().dispatch(request, *args, **kwargs)
