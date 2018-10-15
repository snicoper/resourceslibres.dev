from django.conf.urls import url

from . import views

app_name = 'contact'

urlpatterns = [

    # Form de contacto.
    url(
        regex=r'^$',
        view=views.ContactView.as_view(),
        name='contact'
    ),

    # Lista de mensajes de contacto.
    url(
        regex=r'^list/$',
        view=views.ContactMessageListView.as_view(),
        name='list'
    ),

    # Detalles de mensaje de contacto.
    url(
        regex=r'^details/(?P<pk>\d+)/$',
        view=views.ContactMessageDetailView.as_view(),
        name='details'
    ),
]
