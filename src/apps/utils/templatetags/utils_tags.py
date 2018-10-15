from django import template
from django.utils.html import escape
from django.utils.safestring import mark_safe

import markdown2

register = template.Library()


@register.simple_tag(name='markdown')
def markdown_format(text, safe=False):
    """Devuelve el texto markdown en HTML.

    Por defecto, materializecss elimina los 'estilos'
    de las listas, el replace, es solo útil si se
    esta usando materializecss.

    Example:
        Con un texto seguro.
        {% markdown resource.description safe=True %}
        {% markdown resource.description True %}

        Con un texto inseguro.
        {% markdown resource.description safe=False %}
        {% markdown resource.description False %}
        {% markdown resource.description %}

    Args:
        text (str): Texto markdown
        safe (bool): El texto es seguro? de lo contrario lo escapa.

    Returns:
        str: El markdown convertido en HTML.
    """
    if not safe:
        # Si no es safe, el texto siempre se escapa.
        text = escape(text)
    return mark_safe(
        markdown2.markdown(
            text,
            extras=['fenced-code-blocks']
        )
    )


@register.simple_tag(name='next_pagination', takes_context=True)
def next_pagination(context):
    """La paginación se hace en función de si tiene un query en GET.

    Para paginación, pagina siguiente si existe.

    Example:
        <a href="{% next_pagination %}">next</a>

    Si en el query de una URI existe ?page=xx, cambiara solo la parte
    del ?page=xxx por el nuevo numero de pagina. En caso contrario,
    añadira page=xxx al query string.
    """
    request = context['request']
    page_obj = context['page_obj']
    uri = request.GET.urlencode()
    if not uri:
        return '?page={}'.format(page_obj.next_page_number())
    if 'page' in uri:
        page = 'page={}'.format(page_obj.number)
        new_uri = uri.replace(page, 'page={}'.format(page_obj.next_page_number()))
        return '?{}'.format(new_uri)
    else:
        return '?{}&page={}'.format(uri, page_obj.next_page_number())


@register.simple_tag(name='previous_pagination', takes_context=True)
def previous_pagination(context):
    """La paginación se hace en función de si tiene un query en GET.

    Para paginación, pagina previa si existe.

    Example:
        <a href="{% previous_pagination %}">previous</a>

    Si en el query de una URI existe ?page=xx, cambiara solo la parte
    del ?page=xxx por el nuevo numero de pagina. En caso contrario,
    añadira page=xxx al query string.
    """
    request = context['request']
    page_obj = context['page_obj']
    uri = request.GET.urlencode()
    if not uri:
        return '?page={}'.format(page_obj.previous_page_number())
    if 'page' in uri:
        page = 'page={}'.format(page_obj.number)
        new_uri = uri.replace(page, 'page={}'.format(page_obj.previous_page_number()))
        return '?{}'.format(new_uri)
    else:
        return '?{}&page={}'.format(uri, page_obj.previous_page_number())
