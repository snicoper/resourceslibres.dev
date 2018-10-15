from .base_test import BaseTestCase


class FixturesTest(BaseTestCase):
    """Comprueba que los fixtures se han creado."""

    def test_users_count(self):
        """Numero de usuarios."""
        self.assertEqual(self.user_model.objects.count(), 2)
