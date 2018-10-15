from django.conf.urls import url

from . import api, views

app_name = 'favorites'

urlpatterns = [

    # Pagina principal de favoritos.
    url(
        regex=r'^list/$',
        view=views.FavoriteListView.as_view(),
        name='list'
    ),

    # Favoritos del usuario por categorías.
    url(
        regex=r'^user/(?P<slug>[\w\-]+)/category/(?P<category_slug>[\w\-]+)/list/$',
        view=views.FavoriteByCategoryListView.as_view(),
        name='list_by_category'
    ),

    # Favoritos del usuario por etiquetas.
    url(
        regex=r'^user/(?P<slug>[\w\-]+)/tag/(?P<tag_slug>[\w\-]+)/list/$',
        view=views.FavoriteByTagListView.as_view(),
        name='list_by_tag'
    ),

    # Eliminar todos los favoritos de un usuario.
    url(
        regex=r'^delete/all/$',
        view=views.FavoriteUserListDeleteView.as_view(),
        name='delete_all'
    ),
]

# API
urlpatterns += [

    # Añade un favorito.
    url(
        regex=r'^api/add/$',
        view=api.FavoriteAddApiView.as_view(),
        name='api_add'
    ),

    # Eliminar un favorito.
    url(
        regex=r'^api/remove/$',
        view=api.FavoriteRemoveApiView.as_view(),
        name='api_remove'
    ),
]
