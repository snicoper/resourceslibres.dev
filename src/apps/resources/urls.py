from django.conf.urls import url

from . import api, views

app_name = 'resources'

urlpatterns = [

    # Lista de recursos.
    url(
        regex=r'^$',
        view=views.ResourceListView.as_view(),
        name='list'
    ),

    # Lista de recursos por categoría.
    url(
        regex=r'^category/(?P<category>[\w\-]+)/list/$',
        view=views.ResourcesByCategoryListView.as_view(),
        name='list_by_category'
    ),

    # Lista de recursos por etiqueta.
    url(
        regex=r'^tag/(?P<tag>[\w\-]+)/list/$',
        view=views.ResourcesByTagListView.as_view(),
        name='list_by_tag'
    ),

    # Lista publica de recursos de un usuario.
    url(
        regex=r'^user/(?P<slug>[\w\-]+)/list/$',
        view=views.ResourcesPublicUserListView.as_view(),
        name='public_user_list'
    ),

    # Lista privada de recursos de un usuario, para poderlos administrar.
    url(
        regex=r'^user/(?P<slug>[\w\-]+)/private/list/$',
        view=views.ResourcesPrivateListView.as_view(),
        name='private_user_list'
    ),

    # Lista publica de recursos de un usuario por categoria.
    url(
        regex=r'^user/(?P<slug>[\w\-]+)/category/(?P<category_slug>[\w\-]+)/list/$',
        view=views.ResourcesPublicUserByCategoryListView.as_view(),
        name='public_user_list_by_category'
    ),

    # Lista privada de recursos de un usuario por categoria.
    url(
        regex=r'^user/(?P<slug>[\w\-]+)/category/(?P<category_slug>[\w\-]+)/private/list/$',
        view=views.ResourcesPrivateByCategoryListView.as_view(),
        name='private_user_category_list'
    ),

    # Lista publica de recursos de un usuario por etiqueta.
    url(
        regex=r'^user/(?P<slug>[\w\-]+)/tag/(?P<tag_slug>[\w\-]+)/list/$',
        view=views.ResourcesPublicUserByTagListView.as_view(),
        name='public_user_list_by_tag'
    ),

    # Lista privada de recursos de un usuario por etiqueta.
    url(
        regex=r'^user/(?P<slug>[\w\-]+)/tag/(?P<tag_slug>[\w\-]+)/private/list/$',
        view=views.ResourcesPrivateByTagListView.as_view(),
        name='private_user_tag_list'
    ),

    # Muestra una lista para aprobar recursos (superuser).
    url(
        regex=r'^approve/$',
        view=views.ResourceApproveListView.as_view(),
        name='approve'
    ),

    # Muestra una lista de marked_broken > 0 (superuser).
    url(
        regex=r'^broken/superuser/$',
        view=views.ResourceAdminBrokenLinksView.as_view(),
        name='broken_links_superuser'
    ),

    # Muestra una lista de marked_broken > 0 (owner).
    url(
        regex=r'^broken/list/$',
        view=views.ResourceOwnerBrokenLinksView.as_view(),
        name='broken_links_owner'
    ),

    # Muestra una lista de marked_broken > 0 (owner).
    url(
        regex=r'^spam/list/$',
        view=views.ResourceSuperuserSpamView.as_view(),
        name='spam_links'
    ),

    # Detalles de un recurso.
    url(
        regex=r'^details/(?P<slug>[\w\-]+)/$',
        view=views.ResourceDetailsView.as_view(),
        name='details'
    ),

    # Muestra información del recurso al usuario (owner/superuser).
    url(
        regex=r'^info/(?P<slug>[\w\-]+)/$',
        view=views.ResourceInfoView.as_view(),
        name='info'
    ),

    # Incrementa en 1 clicks y redirecciona al link del recurso.
    url(
        regex=r'^link/(?P<slug>[\w\-]+)/$',
        view=views.ResourceRedirectLinkView.as_view(),
        name='link'
    ),

    # Crear un nuevo recurso.
    url(
        regex=r'^create/$',
        view=views.ResourceCreateView.as_view(),
        name='create'
    ),

    # Actualiza un recurso.
    url(
        regex=r'^update/(?P<slug>[\w\-]+)/$',
        view=views.ResourceUpdateView.as_view(),
        name='update'
    ),

    # Usuario elimina un recurso.
    url(
        regex=r'^delete/(?P<slug>[\w\-]+)/$',
        view=views.ResourceDeleteView.as_view(),
        name='delete'
    ),

    # Crear un nuevo recurso temporal.
    url(
        regex=r'^quick/create/$',
        view=views.QuickResourceCreateView.as_view(),
        name='quick_create'
    ),

    # Lista de recursos rápidos (superuser).
    url(
        regex=r'^quick/list/$',
        view=views.QuickResourceListView.as_view(),
        name='quick_list'
    ),

    # Form para aprobar un recurso rapido (superuser).
    url(
        regex=r'^quick/approve/(?P<pk>\d+)/$',
        view=views.QuickResourceApproveFormView.as_view(),
        name='quick_approve'
    ),
]

# API
urlpatterns += [

    # Votar el recurso.
    url(
        regex=r'^api/rating/(?P<resource_id>\d+)/',
        view=api.ResourceRatingApiView.as_view(),
        name='api_rating_resource'
    ),

    # Marcar un recurso como roto.
    url(
        regex=r'^api/broken/(?P<resource_id>\d+)/',
        view=api.BrokenResourceApiView.as_view(),
        name='api_broken_resource'
    ),

    # Marcar un recurso como spam.
    url(
        regex=r'^api/spam/(?P<resource_id>\d+)/',
        view=api.SpamResourceApiView.as_view(),
        name='api_spam_resource'
    ),

    # Clear marked_broken de un recurso.
    url(
        regex=r'^api/clear/broken/(?P<pk>\d+)/',
        view=api.BrokenLinksSolvedApiView.as_view(),
        name='api_clear_broken_resource'
    ),

    # Clear marked_spam de un recurso.
    url(
        regex=r'^api/clear/spam/(?P<pk>\d+)/',
        view=api.SpamSolvedApiView.as_view(),
        name='api_clear_spam_resource'
    ),
]
