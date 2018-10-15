from haystack.generic_views import SearchView
from haystack.query import SearchQuerySet


class ResourceSearchView(SearchView):
    template_name = 'search/search_resources.html'
    queryset = SearchQuerySet().order_by('-create_at')
    paginate_by = 10
