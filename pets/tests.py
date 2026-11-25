from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from pets.models import Pet

User = get_user_model()


class PetTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('petowner', password='SecurePass123!')
        self.client.force_login(self.user)

    def test_pet_create_and_detail(self):
        response = self.client.post(
            reverse('pets:pet_create'),
            data={
                'name': 'Р‘Р°СЂСЃРёРє',
                'species': 'dog',
                'breed': 'Р”РѕРі',
                'sex': 'male',
                'weight': '12.5',
                'description': 'Р”РѕР±СЂС‹Р№ РїС‘СЃ',
            },
        )
        self.assertEqual(response.status_code, 302)
        pet = Pet.objects.get(name='Р‘Р°СЂСЃРёРє')
        response = self.client.get(reverse('pets:pets_detail', args=[pet.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Р‘Р°СЂСЃРёРє')

    def test_pets_list_requires_login(self):
        self.client.logout()
        response = self.client.get(reverse('pets:pets_list'))
        self.assertEqual(response.status_code, 302)

    def test_cannot_see_other_users_pets(self):
        other = User.objects.create_user('other', password='SecurePass123!')
        Pet.objects.create(owner=other, name='Р§СѓР¶РѕР№')
        response = self.client.get(reverse('pets:pets_list'))
        self.assertNotContains(response, 'Р§СѓР¶РѕР№')
