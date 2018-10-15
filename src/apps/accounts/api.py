from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import HttpResponse, get_object_or_404
from django.views import generic

from .models import UserKarma

UserModel = get_user_model()


class KarmaAddPositeApiView(LoginRequiredMixin, generic.View):
    """Incrementar en 1 los votos positivos de un usuario."""

    def post(self, request, *args, **kwargs):
        user_karma = get_object_or_404(UserModel, pk=kwargs.get('pk'))
        UserKarma.objects.vote_positive(user_karma, request.user)
        return HttpResponse('OK')


class KarmaAddNegativeApiView(LoginRequiredMixin, generic.View):
    """Incrementar en 1 los votos negativos de un usuario."""

    def post(self, request, *args, **kwargs):
        user_karma = get_object_or_404(UserModel, pk=kwargs.get('pk'))
        UserKarma.objects.vote_negative(user_karma, request.user)
        return HttpResponse('OK')
