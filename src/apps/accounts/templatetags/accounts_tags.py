from django import template

from accounts.models import UserKarma
from contact.models import ContactMessage
from resources.models import QuickResource, Resource

register = template.Library()


@register.simple_tag(takes_context=True)
def user_has_vote_user_karma(context, user_karma):
    """Obtener si un usuario ha votado a otro.

    Example:
        {% user_has_vote_user_karma user_karma as karma %}
        {% if karma == 'positive' %} deep-purple lighten-3{% endif %}

    Args:
        user_karma (User): Usuario ha comprobar si ha sido votado.

    Returns:
        str|bool: Si ha sido votado 'positive', si no ha sido votado
        'negative' y si el usuario no esta autenticado, no ha votado
        sobre el usuario o si son el mismo usuario False.
    """
    user = context['request'].user
    if not user.is_authenticated or user == user_karma:
        return False
    try:
        karma = UserKarma.objects.get(user_receiver=user_karma, user_vote=user)
    except UserKarma.DoesNotExist:
        return False
    return 'positive' if karma.positive > 0 else 'negative'


@register.simple_tag
def get_num_approve_resources():
    """Obtener el numero de recursos que están por aprobar."""
    return Resource.objects.filter(active=False).count()


@register.simple_tag
def get_num_quick_resources():
    """Obtener el numero de quick recursos pendientes."""
    return QuickResource.objects.count()


@register.simple_tag
def get_num_broken_links_resources():
    """Obtener el numero de recursos marcados como rotos."""
    return Resource.objects.filter(marked_broken__gt=0).count()


@register.simple_tag
def get_num_spam_resources():
    """Obtener el numero de recursos marcados como spam."""
    return Resource.objects.filter(marked_spam__gt=0).count()


@register.simple_tag
def get_num_messages_unread():
    """Obtener el numero de recursos marcados como spam."""
    return ContactMessage.objects.filter(read=False).count()
