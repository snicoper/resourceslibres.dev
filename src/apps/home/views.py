from django.views import generic


class IndexView(generic.TemplateView):
    """Pagina de prueba para home."""
    template_name = 'home/index.html'

    def get(self, request, *args, **kwargs):
        """Prueba de messages."""
        return super().get(request, *args, **kwargs)
