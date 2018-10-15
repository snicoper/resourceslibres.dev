from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import HttpResponseRedirect, get_object_or_404
from django.urls import reverse
from django.views import generic

from resources.models import Resource

from .models import Favorite


class FavoriteListView(LoginRequiredMixin, generic.ListView):
    """Lista privada de favoritos."""
    template_name = 'favorites/list.html'
    context_object_name = 'favorite_list'
    paginate_by = 10
    model = Favorite

    def get_queryset(self):
        if self.queryset is None:
            self.queryset = Resource.objects.published_with_ratio(
                favorites_resource__user=self.request.user
            )
        return self.queryset


class FavoriteByCategoryListView(FavoriteListView):
    """Favoritos del usuario por categorías."""

    def get_queryset(self):
        slug = self.kwargs.get('category_slug')
        return super().get_queryset().filter(categories__slug=slug)


class FavoriteByTagListView(FavoriteListView):
    """Favoritos del usuario por etiquetas."""

    def get_queryset(self):
        slug = self.kwargs.get('tag_slug')
        return super().get_queryset().filter(tags__slug=slug)


class FavoriteUserListDeleteView(LoginRequiredMixin, generic.DeleteView):
    """Eliminar lista de favoritos de un Usuario."""
    template_name = 'favorites/delete_all.html'
    context_object_name = 'favorite_list'
    model = Favorite

    def get_object(self):
        """Obtener el Favorite según Usuario."""
        return get_object_or_404(Favorite, user=self.request.user)

    def delete(self, request, *args, **kwargs):
        """Si viene del form, eliminar los recursos de favoritos."""
        favorites = self.get_object()
        favorites_list = favorites.resources.all()
        if favorites_list:
            for favorite in favorites_list:
                favorites.resources.remove(favorite)
            msg_success = 'Se han eliminado todos los recursos de favoritos.'
            messages.success(request, msg_success)
        else:
            msg_info = 'No hay favoritos para eliminar'
            messages.info(request, msg_info)
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('favorites:list')
