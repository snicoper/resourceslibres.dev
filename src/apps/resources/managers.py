from django.db import models


class ResourceManager(models.Manager):

    def published(self, **kwargs):
        """Obtener los recurso active=True.

        Args:
            kwargs: key=value para el filter (opcional)
        """
        return self.get_queryset().filter(active=True, **kwargs)

    def with_ratio(self, **kwargs):
        """Obtener la lista de recursos.

        Añade el campo ratio en cada recurso.
        """
        if kwargs:
            queryset = self.get_queryset().filter(**kwargs)
        else:
            queryset = self.get_queryset()
        return queryset.select_related(
            'owner',
            'main_tag',
        ).prefetch_related(
            'categories',
            'tags',
            'ratio_resource'
        ).annotate(ratio=models.Avg('ratio_resource__score'))

    def published_with_ratio(self, **kwargs):
        """Obtener la lista de recursos active=True

        Añade el campo ratio en cada recurso.
        """
        return self.with_ratio(active=True, **kwargs)


class RatioManager(models.Manager):

    def get_ratio_for_resource(self, resource):
        """Obtener el ratio de un recurso.

        Args:
            resource (Resource): Objeto Resource.

        Returns:
            float|int: Numero decimal en caso de tener media, 0 en caso de no tener
            ninguna punctuation.
        """
        ratio = self.get_queryset().filter(resource=resource).aggregate(models.Avg('score'))
        if ratio['score__avg']:
            return ratio['score__avg']
        return 0
