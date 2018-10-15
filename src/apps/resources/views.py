from django.conf import settings
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.sites.shortcuts import get_current_site
from django.db.models import F
from django.shortcuts import Http404, get_object_or_404, redirect
from django.urls import reverse
from django.views import generic

from utils.http import get_full_path, get_http_host
from utils.mail import send_templated_mail
from utils.mixins.views import (
    OwnerOrSuperuserRequiredMixin, SuperuserRequiredMixin,
)

from .forms import QuickResourceCreateForm, ResourceCreateForm
from .models import QuickResource, Resource

UserModel = get_user_model()


class ResourceListView(generic.ListView):
    """Lista de recursos activos."""
    template_name = 'resources/list.html'
    context_object_name = 'resource_list'
    model = Resource
    paginate_by = 10

    def get_queryset(self):
        return self.model.objects.published_with_ratio()


class ResourcesByCategoryListView(ResourceListView):
    """Lista de recursos activos de una categoría concreta."""

    def get_queryset(self):
        category = self.kwargs.get('category')
        return self.model.objects.published_with_ratio().filter(categories__slug=category)


class ResourcesByTagListView(ResourceListView):
    """Lista de recursos activos de un Tag concreto."""

    def get_queryset(self):
        tag = self.kwargs.get('tag')
        return self.model.objects.published_with_ratio().filter(tags__slug=tag)


class ResourcesPublicUserListView(ResourceListView):
    """Lista publica de recursos activos de un usuario."""
    template_name = 'resources/list_user_public.html'

    def get_queryset(self):
        slug = self.kwargs.get('slug')
        return self.model.objects.published_with_ratio().filter(owner__slug=slug)

    def get_context_data(self, **kwargs):
        """Añadir en contexto el owner del queryset.

        Si queryset tiene resultados, obtenemos el owner del primer recurso
        y ahorramos una consulta.
        En caso contrario, obtenemos directamente el owner del slug.
        Si no hay resultados y no existe un usuario con el slug, lanzara Http404.
        """
        context = super().get_context_data(**kwargs)
        queryset = self.get_queryset()
        if queryset.exists():
            context['owner'] = queryset[0].owner
        else:
            context['owner'] = get_object_or_404(UserModel, slug=self.kwargs.get('slug'))
        return context


class ResourcesPrivateListView(LoginRequiredMixin, ResourceListView):
    """Lista de recursos privados de un usuario.

    Muestra los recursos actives True y False
    """
    template_name = 'resources/list_user_private.html'

    def get_queryset(self):
        queryset = self.model.objects.with_ratio().filter(
            owner=self.request.user
        ).prefetch_related('favorites_resource')
        if not queryset:
            return queryset
        return queryset


class ResourcesPublicUserByCategoryListView(ResourcesPublicUserListView):
    """Lista publica de un usuario por una categoría concreta."""

    def get_queryset(self):
        return super().get_queryset().filter(categories__slug=self.kwargs.get('category_slug'))


class ResourcesPrivateByCategoryListView(ResourcesPrivateListView):
    """Lista de recursos privados de un usuario, muestra una categoria."""

    def get_queryset(self):
        return super().get_queryset().filter(
            categories__slug=self.kwargs.get('slug')
        )


class ResourcesPublicUserByTagListView(ResourcesPublicUserListView):
    """Lista publica de un usuario por una etiqueta concreta."""

    def get_queryset(self):
        return super().get_queryset().filter(tags__slug=self.kwargs.get('tag_slug'))


class ResourcesPrivateByTagListView(ResourcesPrivateListView):
    """Lista de recursos privados de un usuario, muestra una etiqueta."""

    def get_queryset(self):
        return super().get_queryset().filter(
            tags__slug=self.kwargs.get('slug')
        )


class ResourceApproveListView(SuperuserRequiredMixin, ResourceListView):
    """Mostrar lista de recursos sin activar a un superuser."""
    template_name = 'resources/list_approve.html'

    def get_queryset(self):
        if self.queryset is None:
            self.queryset = self.model.objects.with_ratio().filter(active=False)
        return self.queryset


class ResourceAdminBrokenLinksView(SuperuserRequiredMixin, ResourceListView):
    """Muestra al superuser la lista de resources marcados con links rotos."""
    template_name = 'resources/list_broken_links.html'

    def get_queryset(self):
        if self.queryset is None:
            self.queryset = self.model.objects.with_ratio().filter(marked_broken__gte=1)
        return self.queryset


class ResourceOwnerBrokenLinksView(LoginRequiredMixin, ResourceListView):
    """Muestra al owner la lista de resources marcados con links rotos."""
    template_name = 'resources/list_broken_links.html'

    def get_queryset(self):
        if self.queryset is None:
            self.queryset = self.model.objects.with_ratio().filter(
                marked_broken__gte=1,
                owner=self.request.user
            )
        return self.queryset


class ResourceSuperuserSpamView(SuperuserRequiredMixin, ResourceListView):
    """Muestra al superuser la lista de recursos marcados como Spam."""
    template_name = 'resources/list_spam_links.html'

    def get_queryset(self):
        if self.queryset is None:
            self.queryset = self.model.objects.with_ratio().filter(marked_spam__gte=1)
        return self.queryset


class ResourceDetailsView(generic.DetailView):
    """Detalles de un recurso.

    Si el recurso esta active False, solo se mostrara si es el owner o
    superuser, de lo contrario, requiere siempre active True.

    Incrementara + 1 el campo views, siempre que no sea el owner
    o superuser del recurso.
    """
    template_name = 'resources/details.html'
    context_object_name = 'resource'
    model = Resource

    def get_object(self, queryset=None):
        slug = self.kwargs.get(self.slug_url_kwarg)
        if self.queryset is None:
            self.queryset = self.model.objects.with_ratio(slug=slug)
            if not self.queryset:
                raise Http404
            if self.queryset[0].owner != self.request.user and not self.request.user.is_superuser:
                # Si no es owner o superuser raise Http404 si no esta activo.
                if not self.queryset[0].active:
                    raise Http404
                # Incrementar +1 las vistas del recurso.
                self.get_queryset().filter(slug=slug).update(views=F('views') + 1)
        return self.queryset[0]


class ResourceInfoView(LoginRequiredMixin, OwnerOrSuperuserRequiredMixin, generic.DetailView):
    """Información del recurso al owner o superuser del recurso.

    Muestra una pequñas stats sobre el recurso.
    """
    template_name = 'resources/resource_info.html'
    context_object_name = 'resource'
    model = Resource

    def get_object(self, queryset=None):
        slug = self.kwargs.get(self.slug_url_kwarg)
        if self.queryset is None:
            try:
                self.queryset = self.model.objects.with_ratio(slug=slug)[0]
            except (IndexError, self.model.DoesNotExist):
                raise Http404
        return self.queryset


class ResourceRedirectLinkView(generic.View):
    """Incrementa en 1 el campo clicks y redirecciona al link del recurso."""

    def get(self, request, *args, **kwargs):
        resource = get_object_or_404(Resource, slug=kwargs.get('slug'))
        resource.clicks += 1
        resource.save()
        return redirect(resource.link)


class ResourceCreateView(LoginRequiredMixin, generic.CreateView):
    """Crear un nuevo recurso."""
    template_name = 'resources/create.html'
    form_class = ResourceCreateForm
    model = Resource

    def get_initial(self):
        initial = super().get_initial()
        initial['owner'] = self.request.user
        return initial

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['btn_name'] = 'Crear'
        return context

    def get_success_url(self):
        self._notify_admins()
        msg_success = '¡Recurso creado con éxito!'
        messages.success(self.request, msg_success)
        return super().get_success_url()

    def _notify_admins(self):
        """Notifica a los administradores del nuevo recurso."""
        resource = self.object
        site = get_current_site(self.request)
        context = {
            'site_name': site.name,
            'title': resource.title,
            'resource_link': get_full_path(self.request, 'resources:details', slug=resource.slug),
            'link_resource_admin': '{}/admin/resources/resource/{}/change/'.format(
                get_http_host(self.request),
                resource.pk
            )
        }
        send_templated_mail(
            subject='Se ha creado un nuevo recurso en {}'.format(site.name),
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipients=settings.GROUP_EMAILS['ADMINS'],
            context=context,
            template_text='resources/emails/notify_admins_new_resource.txt'
        )


class ResourceUpdateView(LoginRequiredMixin, OwnerOrSuperuserRequiredMixin, generic.UpdateView):
    """Actualizar un recurso."""
    template_name = 'resources/update.html'
    context_object_name = 'resource'
    form_class = ResourceCreateForm
    model = Resource

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['btn_name'] = 'Actualizar'
        context['resource_update'] = True
        return context

    def get_success_url(self):
        msg_success = '¡Recurso actualizado con éxito!'
        messages.success(self.request, msg_success)
        return super().get_success_url()


class ResourceDeleteView(LoginRequiredMixin, OwnerOrSuperuserRequiredMixin, generic.DeleteView):
    """Eliminar un recurso."""
    template_name = 'resources/delete.html'
    context_object_name = 'resource'
    model = Resource

    def get_success_url(self):
        """Si todo OK, redireccionar al perfil de usuario."""
        msg_success = 'El recurso se ha eliminado con éxito'
        messages.success(self.request, msg_success)
        return reverse('accounts:profile')


class QuickResourceListView(LoginRequiredMixin, SuperuserRequiredMixin, generic.ListView):
    """Lista de recuros rapidos por aprobar, solo para superuser."""
    template_name = 'resources/quick_resource_list.html'
    context_object_name = 'resource_list'
    model = QuickResource
    paginate_by = 20


class QuickResourceCreateView(LoginRequiredMixin, generic.CreateView):
    """Crea un recuro temporal."""
    template_name = 'resources/create.html'
    form_class = QuickResourceCreateForm
    model = QuickResource

    def get_initial(self):
        initial = super().get_initial()
        initial['owner'] = self.request.user
        return initial

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['btn_name'] = 'Crear'
        context['quick_resource'] = True
        return context

    def get_success_url(self):
        self._notify()
        msg_success = '¡Recurso creado con éxito!'
        messages.success(self.request, msg_success)
        return reverse('accounts:profile')

    def _notify(self):
        """Notifica al owner y superuser que se ha creado el recurso."""
        resource = self.object
        site = get_current_site(self.request)
        context = {
            'site_name': site.name,
            'user_name': resource.owner.username,
            'resource_title': resource.title,
            'resource_message': resource.message
        }
        subject = 'Se ha creado el recurso {resource}'.format(resource=resource.title)
        # Notificar a los ADMINS.
        send_templated_mail(
            subject=subject,
            from_email=settings.GROUP_EMAILS['NO-REPLY'],
            recipients=settings.GROUP_EMAILS['ADMINS'],
            context=context,
            template_text='resources/emails/notify_quick_resource_superuser_create.txt'
        )
        # Notificar al owner.
        send_templated_mail(
            subject=subject,
            from_email=settings.GROUP_EMAILS['NO-REPLY'],
            recipients=[resource.owner.email],
            context=context,
            template_text='resources/emails/notify_quick_resource_owner_create.txt'
        )


class QuickResourceApproveFormView(SuperuserRequiredMixin, ResourceCreateView):
    """Aprobar un recurso rápido.

    Muestra el form de creación del un nuevo recurso normal pero
    añade los datos del recurso rápido (obtenidos por el pk del URLConf).

    El superuser, ya ha tenido que crear manualmente los datos que faltaban
    al recurso.
    """

    def get_initial(self):
        """Añade los datos del recurso rápido."""
        quick_resource = get_object_or_404(QuickResource, pk=self.kwargs.get('pk'))
        initial = super().get_initial()
        initial['owner'] = quick_resource.owner.pk
        initial['title'] = quick_resource.title
        initial['link'] = quick_resource.link
        return initial

    def get_success_url(self):
        """Si todo OK, eliminar el recurso rápido."""
        # Poner activo el recurso recién movido/creado.
        Resource.objects.filter(slug=self.object.slug).update(active=True)
        self._notify()
        # Eliminar el recurso rápido.
        QuickResource.objects.get(pk=self.kwargs.get('pk')).delete()
        return super().get_success_url()

    def _notify(self):
        """Notifica al owner que se ha aprobado el recurso."""
        resource = self.object
        site = get_current_site(self.request)
        context = {
            'site_name': site.name,
            'user_name': resource.owner.username,
            'resource_title': resource.title,
            'resource_link': get_full_path(self.request, 'resources:details', slug=resource.slug)
        }
        subject = 'Se ha publicado el recurso {resource}'.format(resource=resource.title)
        send_templated_mail(
            subject=subject,
            from_email=settings.GROUP_EMAILS['NO-REPLY'],
            recipients=[resource.owner.email],
            context=context,
            template_text='resources/emails/notify_quick_resource_approve.txt'
        )
