from haystack import indexes

from resources.models import Resource


class ResourceIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    title = indexes.CharField(model_attr='title')
    main_tag = indexes.CharField(model_attr='main_tag__title')
    tags = indexes.CharField(model_attr='tags__title')
    description = indexes.CharField(model_attr='description')
    create_at = indexes.DateTimeField(model_attr='create_at')

    def get_model(self):
        return Resource

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.published()
