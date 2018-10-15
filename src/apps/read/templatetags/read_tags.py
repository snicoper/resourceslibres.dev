from django import template
from django.db.models import Count

from resources.models import Category, Tag

register = template.Library()


@register.simple_tag(takes_context=True)
def user_has_read_resource(context, resource):
    """Comprueba si un usuario ha leído un recurso.

    Args:
        context (Context): HttpContext, se pasa de manera explicita.
        resource (Resource): El recurso a comprobar.

    Returns:
        bool: True si el usuario ha leído el recurso, False en caso contrario.
    """
    user = context['request'].user
    if not user.is_authenticated:
        return False
    return bool(resource.resources_read.filter(user=user))


@register.inclusion_tag('resources/_sidenav_cats_tags.html', takes_context=True)
def sidenav_read_owner_tags_categories(context, owner):
    """Obtener lista de Category y Tag de leídos en un owner, con el
    numero de resources de cada Category o Tag.

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
        resource_categories__resources_read__user=owner
    ).order_by('title').annotate(
        total=Count('resource_categories')
    )

    tag_list = Tag.objects.filter(
        resource_tags__resources_read__user=owner
    ).order_by('title').annotate(
        total=Count('resource_tags')
    )

    return {
        'MEDIA_URL': context['MEDIA_URL'],
        'owner': owner,
        'category_list': category_list,
        'tag_list': tag_list,
        'category_url': 'read:list_by_category',
        'tag_url': 'read:list_by_tag'
    }
