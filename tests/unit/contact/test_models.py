from .base_contact import BaseContactTest


class ContactMessageTest(BaseContactTest):

    def setUp(self):
        super().setUp()
        self.data = {
            'subject': 'Mensaje test',
            'message': 'Mensaje de prueba',
            'username': 'testuser',
            'email': 'testuser@example.com',
            'is_register': False
        }
        self.message = self.contact_model.objects.create(**self.data)

    def test_nuevo_mensaje(self):
        """Comprueba un nuevo mensaje."""
        self.assertEqual(self.contact_model.objects.count(), 1)

    def test_str(self):
        """Prueba __str__."""
        self.assertEqual(str(self.message), self.data['subject'])

    def test_read_default_false(self):
        """Por defecto read es False."""
        self.assertFalse(self.message.read)
