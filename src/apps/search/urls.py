from django.conf.urls import url

from . import views

app_name = 'search'

urlpatterns = [

    # Búsqueda en los recursos.
    url(
        regex=r'^$',
        view=views.ResourceSearchView.as_view(),
        name='resources'
    ),
]
