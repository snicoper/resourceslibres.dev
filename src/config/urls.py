from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.views.static import serve

from resources.sitemaps import ResourceSitemap
from resources.views import ResourceListView

# Sitemaps
sitemaps = {
    'resources': ResourceSitemap
}

urlpatterns = [
    ##################################################
    # / Home page.
    url(r'^$', ResourceListView.as_view(), name='home_page'),
    ##################################################

    # /accounts/*
    url(r'^accounts/', include('accounts.urls')),

    # /auth/*
    url(r'^auth/', include('authentication.urls')),

    # /contact/*
    url(r'^contact/', include('contact.urls')),

    # /favorites/*
    url(r'^favorites/', include('favorites.urls')),

    # /feeds/*
    url(r'^feeds/', include('feeds.urls')),

    # /pages/*
    url(r'^pages/', include('pages.urls')),

    # /read/*
    url(r'^read/', include('read.urls')),

    # /recommend/*
    url(r'^recommend/', include('recommend.urls')),

    # /resources/*
    url(r'^resources/', include('resources.urls')),

    # /search/*
    url(r'^search/', include('search.urls')),

    # /admin/*
    url(r'^admin/', admin.site.urls),
]

# Sitemaps para anuncios y blog.
urlpatterns.append(
    url(
        regex=r'^sitemap\.xml$',
        view=sitemap,
        kwargs={'sitemaps': sitemaps},
        name='django.contrib.sitemaps.views.sitemap'
    ),
)


if settings.DEBUG:
    # App home solo en desarrollo para pruebas.
    urlpatterns += [
        # /home/*
        url(r'^home/', include('home.urls')),
    ]

    # static files (images, css, javascript, etc.)
    import debug_toolbar

    urlpatterns += [
        # /media/:<mixed>path/
        url(
            regex=r'^media/(?P<path>.*)$',
            view=serve,
            kwargs={'document_root': settings.MEDIA_ROOT}
        ),

        url(r'^__debug__/', include(debug_toolbar.urls)),
    ]
