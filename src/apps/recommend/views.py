from django import forms
from django.contrib import messages
from django.contrib.sites.models import Site
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views import generic

from resources.models import Resource
from utils.http import get_full_path
from utils.mail import send_templated_mail

from .forms import RecommendResourceForm


class RecommendResourceView(generic.FormView):
    template_name = 'recommend/resource.html'
    form_class = RecommendResourceForm

    def get_form(self, form_class=None):
        """Si el usuario esta autenticado, ocultar campo from_email."""
        form = super().get_form(form_class)
        if self.request.user.is_authenticated:
            form.fields['from_email'].widget = forms.HiddenInput()
        return form

    def get_initial(self):
        """Si el usuario esta autenticado, campo from_email poner email."""
        initial = super().get_initial()
        if self.request.user.is_authenticated:
            initial['from_email'] = self.request.user.email
        return initial

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['resource'] = get_object_or_404(Resource, slug=self.kwargs.get('slug'))
        return context

    def form_valid(self, form):
        """Si el form es valido, mandar el email al recipient."""
        resource = Resource.objects.get(slug=self.kwargs.get('slug'))
        site = Site.objects.get_current()
        from_email = form.cleaned_data.get('from_email')
        recipients = [form.cleaned_data.get('recipient_email')]
        message = form.cleaned_data.get('message')
        subject = 'Recomendación de un recurso en {}'.format(site.name)
        resource_link = get_full_path(
            self.request,
            'resources:details',
            slug=resource.slug
        )
        context = {
            'site_name': site.name,
            'resource_title': resource.title,
            'from_email': from_email,
            'message': message,
            'resource_link': resource_link
        }
        send_templated_mail(
            subject=subject,
            from_email=from_email,
            recipients=recipients,
            context=context,
            template_text='recommend/emails/resource.txt'
        )
        return super().form_valid(form)

    def get_success_url(self):
        """Redirecciona a detalles del recurso."""
        msg_success = 'El recurso se ha enviado con éxito'
        messages.success(self.request, msg_success)
        return reverse('resources:details', kwargs={'slug': self.kwargs.get('slug')})
