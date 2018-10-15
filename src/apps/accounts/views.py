from django import forms
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views import generic

from .forms import UserUpdateAvatarForm
from .models import User


class ProfileIndexView(LoginRequiredMixin, generic.TemplateView):
    """Perfil privado del usuario."""
    template_name = 'accounts/profile.html'


class ProfilePublicView(generic.DetailView):
    """Perfil publico de un usuario."""
    template_name = 'accounts/profile_public.html'
    context_object_name = 'profile'
    model = User


class UserAvatarUpdateView(LoginRequiredMixin, generic.UpdateView):
    """Añadir/Actualizar avatar de usuario."""
    template_name = 'accounts/avatar_update.html'
    form_class = UserUpdateAvatarForm
    model = User

    def get_object(self, queryset=None):
        """Obtener avatar del usuario actual."""
        return get_object_or_404(self.model, pk=self.request.user.pk)

    def get_form(self, form_class=None):
        """Ocultar field delete_avatar si el usuario no tiene avatar."""
        form = super().get_form(form_class)
        if not self.request.user.avatar:
            form.fields['delete_avatar'].widget = forms.HiddenInput()
        return form

    def form_valid(self, form):
        """Resetear avatar si pulsa marca delete_avatar.

        Si el usuario ha pulsado en delete_avatar, el campo avatar
        se pondrá en '', por lo que restablecerá el valor por defecto.
        """
        if form.cleaned_data['delete_avatar']:
            instance = form.save(commit=False)
            instance.avatar = ''
        return super().form_valid(form)

    def get_success_url(self):
        msg_success = 'Se ha actualizado el avatar'
        messages.success(self.request, msg_success)
        return reverse('accounts:profile')
