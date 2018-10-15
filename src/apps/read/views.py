from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.views import generic

from .models import ReadUserResources


class ReadUserResourcesListView(LoginRequiredMixin, generic.ListView):
    """Muestra la lista de recursos leídos por el usuario actual."""
    context_object_name = 'resource_list'
    template_name = 'read/list.html'
    model = ReadUserResources
    paginate_by = 10

    def get_queryset(self):
        """Obtener queryset con la lista de recursos leídos.

        NOTA: En el template, marca consultas como duplicadas, eso es debido
        a que read/list.html llama a su ves a read/_resource_read_unread.html
        y tiene una consulta duplicadas para obtener si el recurso lo ha
        marcado como leído el usuario (src/apps/read/templatetags/read_tags.py).
        Lo asumo pero no le doy mucha importancia.
        """
        read_obj = get_object_or_404(self.model, user=self.request.user)
        return read_obj.resources.published()


class ReadUserResourceByCategoryListView(ReadUserResourcesListView):
    """Muestra la lista de recursos de una categoría leídos por el usuario actual."""

    def get_queryset(self):
        return super().get_queryset().filter(
            categories__slug=self.kwargs.get('category_slug')
        )


class ReadUserResourceByTagListView(ReadUserResourcesListView):
    """Muestra la lista de recursos de una etiqueta leídos por el usuario actual."""

    def get_queryset(self):
        return super().get_queryset().filter(
            tags__slug=self.kwargs.get('tag_slug')
        )
