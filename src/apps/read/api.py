from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import Http404, HttpResponse, get_object_or_404
from django.views import generic

from resources.models import Resource

from .models import ReadUserResources


class UserMarksResourceRead(LoginRequiredMixin, generic.View):
    """Un usuario marca un recurso como leído."""

    def post(self, request, *args, **kwargs):
        if not request.is_ajax():
            raise Http404
        resource_id = kwargs.get('resource_id')
        resources_read = get_object_or_404(ReadUserResources, user=request.user)
        resource = get_object_or_404(Resource, pk=resource_id)
        # Si ya lo tiene marcado como leido, Http404
        if resource in resources_read.resources.all():
            raise Http404
        resources_read.resources.add(resource)
        return HttpResponse('OK')


class UserMarksResourceUnread(LoginRequiredMixin, generic.View):
    """Un usuario marca un recurso como no leído."""

    def post(self, request, *args, **kwargs):
        if not request.is_ajax():
            raise Http404
        resource_id = kwargs.get('resource_id')
        resources_read = get_object_or_404(ReadUserResources, user=request.user)
        resource = get_object_or_404(Resource, pk=resource_id)
        # Si no lo lo tenia como leido, Http404
        if resource not in resources_read.resources.all():
            raise Http404
        resources_read.resources.remove(resource)
        return HttpResponse('OK')
