from django.conf.urls import url

from . import api, views

app_name = 'accounts'

urlpatterns = [

    # Perfil de usuario.
    url(
        regex=r'^profile/$',
        view=views.ProfileIndexView.as_view(),
        name='profile'
    ),

    # Perfil de usuario.
    url(
        regex=r'^profile/user/(?P<slug>[\w\-]+)/$',
        view=views.ProfilePublicView.as_view(),
        name='profile_public'
    ),

    # Cambiar/añadir avatar de usuario.
    url(
        regex=r'^avatar/update/$',
        view=views.UserAvatarUpdateView.as_view(),
        name='avatar_update'
    ),
]

# API
urlpatterns += [

    # Aumentar en 1 el karma positivo de un usuario.
    url(
        regex=r'^api/karma/positive/(?P<pk>\d+)/$',
        view=api.KarmaAddPositeApiView.as_view(),
        name='api_karma_add_positive'
    ),

    # Aumentar en 1 el karma negativo de un usuario.
    url(
        regex=r'^api/karma/negative/(?P<pk>\d+)/$',
        view=api.KarmaAddNegativeApiView.as_view(),
        name='api_karma_add_negative'
    ),
]
