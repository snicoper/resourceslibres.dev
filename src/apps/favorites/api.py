from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import Http404, HttpResponse, get_object_or_404
from django.views import generic

from .models import Resource


class FavoriteAddApiView(LoginRequiredMixin, generic.View):
    """Añade un favorito vía AJAX."""

    def post(self, request, *args, **kwargs):
        """En AJAX se ha de pasar el ID del resource."""
        if not request.is_ajax():
            raise Http404
        resource_id = request.POST.get('resource_id')
        resource = get_object_or_404(Resource, pk=resource_id)
        try:
            favorites = request.user.favorites_user
            if resource not in favorites.resources.all():
                favorites.resources.add(resource)
        except:
            return HttpResponse('BAD')
        return HttpResponse('OK')


class FavoriteRemoveApiView(LoginRequiredMixin, generic.View):
    """Elimina un favorito vía AJAX."""

    def post(self, request, *args, **kwargs):
        """En AJAX se ha de pasar el ID del resource."""
        if not request.is_ajax():
            raise Http404
        resource_id = request.POST.get('resource_id')
        resource = get_object_or_404(Resource, pk=resource_id)
        try:
            favorites = request.user.favorites_user
            if resource in favorites.resources.all():
                favorites.resources.remove(resource)
        except:
            return HttpResponse('BAD')
        return HttpResponse('OK')
