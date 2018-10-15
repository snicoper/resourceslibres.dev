from django.db import models


class UserKarmaManager(models.Manager):
    """Manager de UserKarma."""

    def get_positives_for_user(self, user):
        """Obtener la suma total de positivos de un usuario."""
        return self.get_queryset().filter(
            user_receiver=user,
            positive=1
        ).aggregate(total=models.Sum('positive')).get('total') or 0

    def get_negatives_for_user(self, user):
        """Obtener la suma total de negativos de un usuario."""
        return self.get_queryset().filter(
            user_receiver=user,
            negative=1
        ).aggregate(total=models.Sum('negative')).get('total') or 0

    def vote_positive(self, user_receiver, user_vote):
        """Un usuario vota a otro usuario con un positivo.

        Args:
            user_receiver (User): Usuario que obtendrá el voto positivo.
            user_vote (User): Usuario que da el positivo.

        Returns:
            QuerySet|False: QuerySet si todo OK, False si es el mismo usuario.
        """
        if user_vote == user_receiver:
            return False
        queryset = self.get_or_create(user_receiver=user_receiver, user_vote=user_vote)[0]
        queryset.positive = 1
        queryset.negative = 0
        queryset.save()
        return queryset

    def vote_negative(self, user_receiver, user_vote):
        """Un usuario vota a otro usuario con un negativo.

        Args:
            user_receiver (User): Usuario que obtendrá el voto negativo.
            user_vote (User): Usuario que da el negativo.

        Returns:
            QuerySet|False: QuerySet si todo OK, False si es el mismo usuario.
        """
        if user_vote == user_receiver:
            return False
        queryset = self.get_or_create(user_receiver=user_receiver, user_vote=user_vote)[0]
        queryset.positive = 0
        queryset.negative = 1
        queryset.save()
        return queryset
