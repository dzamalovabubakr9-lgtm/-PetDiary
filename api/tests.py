from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient, APITestCase

from advice.models import AdviceCategory
from pets.models import Pet

User = get_user_model()


class ApiAuthTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user('apiuser', password='SecurePass123!', email='apiuser@example.com')
        self.pet = Pet.objects.create(owner=self.user, name='Боня')

    def test_pet_crud_with_token(self):
        token = Token.objects.create(user=self.user)
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION=f'Token {token.key}')

        response = client.get(reverse('api_root'))
        self.assertEqual(response.status_code, 200)

        response = client.get('/api/pets/')
        self.assertEqual(response.status_code, 200)

        response = client.post('/api/pets/', data={'name': 'Барсик', 'species': 'dog', 'breed': 'Дог'})
        self.assertEqual(response.status_code, 201)
        pk = response.data['id']

        response = client.get(f'/api/pets/{pk}/')
        self.assertEqual(response.status_code, 200)

        response = client.put(f'/api/pets/{pk}/', data={'name': 'Барсик Б', 'species': 'cat'})
        self.assertEqual(response.status_code, 200)

        response = client.delete(f'/api/pets/{pk}/')
        self.assertEqual(response.status_code, 204)

    def test_unauthenticated_denied(self):
        client = APIClient()
        response = client.get('/api/pets/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_only_own_pets(self):
        other = User.objects.create_user('other', password='SecurePass123!')
        Pet.objects.create(owner=other, name='Чужой')
        token = Token.objects.create(user=self.user)
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION=f'Token {token.key}')
        response = client.get('/api/pets/')
        self.assertEqual(response.status_code, 200)
        names = [pet['name'] for pet in response.data['results']] if isinstance(response.data, dict) else [pet['name'] for pet in response.data]
        self.assertNotIn('Чужой', names)

    def test_advice_read_only(self):
        cat = AdviceCategory.objects.create(name='Советы')
        token = Token.objects.create(user=self.user)
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION=f'Token {token.key}')
        response = client.post('/api/advice/', data={'category': cat.pk, 'title': 'T', 'content': 'C'})
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_diary_api_rejects_foreign_pet(self):
        other = User.objects.create_user('other_diary', password='SecurePass123!')
        foreign_pet = Pet.objects.create(owner=other, name='Чужой питомец')
        token = Token.objects.create(user=self.user)
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION=f'Token {token.key}')
        response = client.post('/api/diary/', data={
            'pet': foreign_pet.pk, 'date': '2026-11-25', 'title': 'Попытка',
            'description': 'Не должно сохраниться', 'category': 'other',
        })
        self.assertEqual(response.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)
