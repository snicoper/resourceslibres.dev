import json
import os

from django.contrib.auth import get_user_model
from django.test import TestCase

UserModel = get_user_model()


class BaseTestCase(TestCase):
    """Utilizadades para todos los tests relacionados con el sitio.

    Incluye Fixtures para los modelos.
        user_model

    Attributes:
        fixtures (list): Nombres de fixtures a leer.
    """
    fixtures = [
        'accounts.json',
        'sites.json'
    ]

    def setUp(self):
        super().setUp()
        self.user_model = UserModel
        self.user = self.user_model.objects.get(pk=1)

    def login(self, username=None, password=None):
        """Login de usuario.

        Si no se pasan username y password usara por defecto self.user.username
        y 123 respectivamente.

        Args:
            username (str): Nombre de usuario.
            password (str): Password de usuario.

        Returns:
            bool: True si loguea, False en caso contrario.
        """
        username = self.user.username if username is None else username
        password = '123' if password is None else password
        return self.client.login(username=username, password=password)

    def logout(self):
        self.client.logout()

    def load_data(self, path_data):
        """Obtener de un .json datos.

        Args:
            path_data (str): path con el archivo a leer.

        Returns:
            dict: Diccionario con los datos del json

        Raises:
            FileNotFoundError: Si no existe el .json en el la ruta indicada.
        """
        if not os.path.exists(path_data):
            raise FileNotFoundError
        with open(path_data, 'r') as fh:
            data = json.load(fh)
        return data
