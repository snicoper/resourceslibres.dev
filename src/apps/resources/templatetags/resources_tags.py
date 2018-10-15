from django import template
from django.db.models import Count

from resources.models import Category, Resource, Tag

register = template.Library()


@register.simple_tag(takes_context=True)
def get_user_score_for_resource(context, resource):
    """Obtener el score de un usuario en un resource.

    Args:
        context (Context): HttpContext
        resource (Resource): El resource a comprobar.

    Returns:
        int: El score del usuario sobre el resource, 0 en caso
        de que el usuario no haya votado sobre el resource.
    """
    request = context['request']
    if not request.user.is_authenticated:
        return 0
    score = resource.ratio_resource.filter(user=request.user)
    if not score:
        return 0
    return score[0].score


@register.inclusion_tag('resources/_sidenav_cats_tags.html', takes_context=True)
def resources_sidenav(context):
    """Obtener lista de Category y Tag, con el numero de resources
    de cada Category o Tag.

    A parte cada item en category_list y tag_list tendrá la propiedad
    'total' con el numero de resources que tiene cada una.

    Se omiten las categorías y tags sin resources.

    Returns:
        Un diccionario con los siguientes elementos:

        MEDIA_URL: String con el valor de settings.MEDIA_URL
        category_list: QuerySet con la lista de categorías
        tag_list: QuerySet con la lista de tags.
        category_url: Parte del URLConf para generar luego el enlace.
        tag_url: Parte del URLConf para generar luego el enlace.
    """
    category_list = Category.objects.annotate(
        total=Count('resource_categories')
    ).filter(total__gt='0').order_by('title')

    tag_list = Tag.objects.annotate(
        total=Count('resource_tags')
    ).filter(total__gt='0').order_by('title')

    return {
        'MEDIA_URL': context['MEDIA_URL'],
        'category_list': category_list,
        'tag_list': tag_list,
        'category_url': 'resources:list_by_category',
        'tag_url': 'resources:list_by_tag'
    }


@register.inclusion_tag('resources/_sidenav_cats_tags.html', takes_context=True)
def resources_public_owner_sidenav(context, owner):
    """Obtener lista publica de Category y Tag de un owner, con el numero de
    resources de cada Category o Tag.

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
        resource_categories__owner=owner
    ).annotate(
        total=Count('resource_categories')
    ).order_by('title')

    tag_list = Tag.objects.filter(
        resource_tags__owner=owner
    ).annotate(
        total=Count('resource_tags')
    ).order_by('title')

    return {
        'MEDIA_URL': context['MEDIA_URL'],
        'owner': owner,
        'category_list': category_list,
        'tag_list': tag_list,
        'category_url': 'resources:public_user_list_by_category',
        'tag_url': 'resources:public_user_list_by_tag',
    }


@register.inclusion_tag('resources/_sidenav_cats_tags.html', takes_context=True)
def resources_private_owner_sidenav(context, owner):
    """Obtener lista publica de Category y Tag de un owner, con el numero de
    resources de cada Category o Tag.

    Cambia category_url y tag_url.

    @see: resources_public_owner_sidenav.
    """
    resource_list = resources_public_owner_sidenav(context, owner)
    resource_list['category_url'] = 'resources:private_user_category_list'
    resource_list['tag_url'] = 'resources:private_user_tag_list'
    return resource_list


@register.simple_tag(takes_context=True)
def get_num_resources_broken(context):
    """Obtener el numero de recursos que han sido marcados como links rotos.

    Returns:
        int: Numero de recursos con links rotos, 0 si no tiene recursos o
        si no tiene recursos con links rotos.

        Si el usuario no esta logueado, también retornara 0.
    """
    user = context['request'].user
    if not user.is_authenticated:
        return 0
    return Resource.objects.filter(owner=user, marked_broken__gt=0).count()
