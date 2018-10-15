from django.conf.urls import url

from . import feeds, views

app_name = 'feeds'

# Feeds
urlpatterns = [

    # Ultimos recursos.
    url(
        regex=r'^$',
        view=feeds.LastedEntriesFeed(),
        name='feed'
    ),

    # Muestra listado de Feeds.
    url(
        regex=r'^list/$',
        view=views.FeedListView.as_view(),
        name='list'
    ),

    # Ultimos recursos por categoria.
    url(
        regex=r'^category/(?P<slug>[\w\-]+)/$',
        view=feeds.LastedEntriesByCategoryFeed(),
        name='feed_by_category'
    ),

    # Ultimos recursos por etiquestas.
    url(
        regex=r'^tag/(?P<slug>[\w\-]+)/$',
        view=feeds.LastedEntriesByTagFeed(),
        name='feed_by_tag'
    ),
]
