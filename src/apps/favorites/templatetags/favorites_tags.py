from django import template
from django.db.models import Count

from resources.models import Category, Tag

register = template.Library()


@register.inclusion_tag('resources/_sidenav_cats_tags.html', takes_context=True)
def sidenav_owner_tags_categories(context, owner):
    """Obtener lista de Category y Tag, con el numero de resources
    de cada Category o Tag de un usuario concreto.

    Las categorías y tags obtenidas son de los favoritos de un usuario.

    A parte cada item en category_list y tag_list tendrá la propiedad
    'total' con el numero de resources que tiene cada una.

    Args:
        owner (User): Usuario a obtener lista de cats y tags.

    Returns:
        Un diccionario con los siguientes elementos:

        MEDIA_URL: String con el valor de settings.MEDIA_URL
        owner (User): Usuario del que se obtiene las listas.
        category_list: QuerySet con la lista de categorías
        tag_list: QuerySet con la lista de tags.
        category_url: Parte del URLConf para generar luego el enlace.
        tag_url: Parte del URLConf para generar luego el enlace.
    """
    category_list = Category.objects.filter(
        resource_categories__favorites_resource__user=owner
    ).order_by('title').annotate(
        total=Count('resource_categories')
    )

    tag_list = Tag.objects.filter(
        resource_tags__favorites_resource__user=owner
    ).order_by('title').annotate(
        total=Count('resource_tags')
    )

    return {
        'MEDIA_URL': context['MEDIA_URL'],
        'owner': owner,
        'category_list': category_list,
        'tag_list': tag_list,
        'category_url': 'favorites:list_by_category',
        'tag_url': 'favorites:list_by_tag'
    }
