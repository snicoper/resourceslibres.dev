from django.views import generic

from resources.models import Category, Tag


class FeedListView(generic.TemplateView):
    """Muestra los feeds a los que se puede sindicar."""
    template_name = 'feeds/list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories_list'] = Category.objects.all()
        context['tags_list'] = Tag.objects.all()
        return context
