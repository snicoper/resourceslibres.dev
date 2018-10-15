from django.conf.urls import url

from . import api, views

app_name = 'read'

urlpatterns = [

    # Muestra la lista de recursos leídos al usuario.
    url(
        regex=r'^list/$',
        view=views.ReadUserResourcesListView.as_view(),
        name='list'
    ),

    # Muestra la lista de recursos leídos al usuario de una categoría concreta.
    url(
        regex=r'^user/(?P<slug>[\w\-]+)/category/(?P<category_slug>[\w\-]+)/list/$',
        view=views.ReadUserResourceByCategoryListView.as_view(),
        name='list_by_category'
    ),

    # Muestra la lista de recursos leídos al usuario de un tag concreto.
    url(
        regex=r'^user/(?P<slug>[\w\-]+)/tag/(?P<tag_slug>[\w\-]+)/list/$',
        view=views.ReadUserResourceByTagListView.as_view(),
        name='list_by_tag'
    ),
]

# API
urlpatterns += [

    # Un usuario marca un recurso como leído.
    url(
        regex=r'^api/read/(?P<resource_id>\d+)/',
        view=api.UserMarksResourceRead.as_view(),
        name='api_user_resource_read'
    ),

    # Un usuario desmarca un recurso como leído.
    url(
        regex=r'^api/unread/(?P<resource_id>\d+)/',
        view=api.UserMarksResourceUnread.as_view(),
        name='api_user_resource_unread'
    ),
]
