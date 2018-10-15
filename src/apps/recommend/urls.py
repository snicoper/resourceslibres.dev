from django.conf.urls import url

from . import views

app_name = 'recommend'

urlpatterns = [

    # Form para recomendar un recurso.
    url(
        regex=r'^resource/(?P<slug>[\w\-]+)/$',
        view=views.RecommendResourceView.as_view(),
        name='resource'
    ),
]
