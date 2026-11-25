from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

User = get_user_model()


class AuthFlowTests(TestCase):
    def test_register_login_logout(self):
        # регистрация
        response = self.client.post(
            reverse('register'),
            data={
                'username': 'testuser',
                'email': 'testuser@example.com',
                'password1': 'SecurePass123!',
                'password2': 'SecurePass123!',
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username='testuser').exists())

        # вход
        response = self.client.post(reverse('login'), data={'username': 'testuser', 'password': 'SecurePass123!'})
        self.assertEqual(response.status_code, 302)
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'testuser', response.content)

        # выход
        self.client.post(reverse('logout'))
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)

    def test_profile_requires_auth(self):
        response = self.client.get(reverse('profile_detail'))
        self.assertEqual(response.status_code, 302)

    def test_profile_edit_requires_auth(self):
        response = self.client.get(reverse('profile_edit'))
        self.assertEqual(response.status_code, 302)

    def test_email_is_unique(self):
        User.objects.create_user('existing', email='taken@example.com', password='SecurePass123!')
        response = self.client.post(reverse('register'), data={
            'username': 'duplicate_email',
            'email': 'taken@example.com',
            'password1': 'SecurePass123!',
            'password2': 'SecurePass123!',
        })
        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.filter(username='duplicate_email').exists())
