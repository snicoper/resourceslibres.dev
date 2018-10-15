from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.sites.models import Site
from django.db.models import F
from django.shortcuts import Http404, HttpResponse, get_object_or_404
from django.views import generic

from utils.http import get_full_path
from utils.mail import send_templated_mail
from utils.mixins.views import SuperuserRequiredMixin

from .models import Ratio, Resource


class ResourceRatingApiView(LoginRequiredMixin, generic.View):
    """Vota un recurso los usuarios autentificados.

    Cuando se ha votado, devuelve el nuevo rating.
    """

    def get(self, request, *args, **kwargs):
        if not request.is_ajax():
            raise Http404
        score = request.GET.get('score')
        resource = get_object_or_404(Resource, pk=kwargs.get('resource_id'))
        ratio_obj = Ratio.objects.filter(user=request.user, resource=resource)
        if ratio_obj:
            ratio_obj.update(score=score)
        else:
            Ratio.objects.create(user=request.user, resource=resource, score=score)
        # Obtener el nuevo ratio.
        new_ratio = Ratio.objects.get_ratio_for_resource(resource)
        return HttpResponse(new_ratio)


class BrokenResourceApiView(generic.View):
    """Reportar un link de recurso como roto.

    El campo Resource.marked_broken se incrementa en 1.
    Después manda al owner del recurso y al los ADMINS un mail informando
    de un link roto.
    """

    def post(self, request, *args, **kwargs):
        if not request.is_ajax():
            raise Http404
        resource_id = kwargs.get('resource_id')
        try:
            Resource.objects.filter(
                pk=resource_id
            ).update(marked_broken=F('marked_broken') + 1)
            self._notify(resource_id)
            return HttpResponse('OK')
        except:
            return HttpResponse('BAD')

    def _notify(self, resource_id):
        """Notifica al owner del recurso y a los ADMINS que el link
        lo han marcado como roto.
        """
        resource = Resource.objects.get(pk=resource_id)
        resource_url = get_full_path(
            self.request,
            'resources:details',
            slug=resource.slug
        )
        site = Site.objects.get_current()
        context = {
            'resource_title': resource.title,
            'resource_url': resource_url,
            'site_name': site.name
        }
        recipients = settings.GROUP_EMAILS['ADMINS']
        recipients += (resource.owner.username, resource.owner.email)
        send_templated_mail(
            subject='Se ha marcado un enlace como roto',
            from_email=settings.GROUP_EMAILS['NO-REPLY'],
            recipients=recipients,
            context=context,
            template_text='resources/emails/notify_marked_resource_broken.txt'
        )


class SpamResourceApiView(generic.View):
    """Reportar un link de recurso como roto.

    El campo Resource.marked_spam se incrementa en 1.
    Después manda un email a los ADMINS del sitio informando de spam.
    """

    def post(self, request, *args, **kwargs):
        if not request.is_ajax():
            raise Http404
        resource_id = kwargs.get('resource_id')
        try:
            Resource.objects.filter(
                pk=resource_id
            ).update(marked_spam=F('marked_spam') + 1)
            self._notify(resource_id)
            return HttpResponse('OK')
        except:
            return HttpResponse('BAD')

    def _notify(self, resource_id):
        """Notifica a la administración que un resource puede ser spam."""
        resource = Resource.objects.get(pk=resource_id)
        resource_url = get_full_path(
            self.request,
            'resources:details',
            slug=resource.slug
        )
        site = Site.objects.get_current()
        context = {
            'resource_title': resource.title,
            'resource_url': resource_url,
            'site_name': site.name
        }
        send_templated_mail(
            subject='Se ha marcado un recurso como SPAM',
            from_email=settings.GROUP_EMAILS['NO-REPLY'],
            recipients=settings.GROUP_EMAILS['ADMINS'],
            context=context,
            template_text='resources/emails/notify_marked_resource_spam.txt'
        )


class BrokenLinksSolvedApiView(LoginRequiredMixin, generic.View):
    """El superuser u owner de un recurso marca como solucionado el link roto.

    Actualizara Resouce.marked_broken = 0.
    """

    def post(self, request, *args, **kwargs):
        if not request.is_ajax():
            raise Http404
        resource = get_object_or_404(Resource, pk=kwargs.get('pk'))
        if not request.user.is_superuser and request.user != resource.owner:
            raise Http404
        Resource.objects.filter(pk=resource.pk).update(marked_broken=0)
        return HttpResponse('OK')


class SpamSolvedApiView(LoginRequiredMixin, SuperuserRequiredMixin, generic.View):
    """El superuser marca como solucionado el link marcado como spam.

    Actualizara Resouce.marked_spam = 0.
    """

    def post(self, request, *args, **kwargs):
        if not request.is_ajax():
            raise Http404
        resource = get_object_or_404(Resource, pk=kwargs.get('pk'))
        Resource.objects.filter(pk=resource.pk).update(marked_spam=0)
        return HttpResponse('OK')
