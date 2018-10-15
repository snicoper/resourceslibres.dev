from django.conf.urls import url

from . import views

app_name = 'pages'

urlpatterns = [

    # Cookies consent.
    url(
        regex=r'^cookie-consent/$',
        view=views.CookieConsentView.as_view(),
        name='cookie_consent'
    ),

    # Términos para añadir un recurso.
    url(
        regex=r'^terms/$',
        view=views.TermsView.as_view(),
        name='terms'
    ),
]
