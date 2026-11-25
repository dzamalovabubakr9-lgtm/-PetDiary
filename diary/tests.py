from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from diary.models import DiaryEntry, DiaryEntryCategory
from pets.models import Pet

User = get_user_model()


class DiaryTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('diaryuser', password='SecurePass123!')
        self.pet = Pet.objects.create(owner=self.user, name='Мурчик')
        self.entry = DiaryEntry.objects.create(
            pet=self.pet, date='2026-11-01', title='Прогулка', description='Прогулялись в парке',
            category=DiaryEntryCategory.WALKS,
        )
        self.client.force_login(self.user)

    def test_diary_list(self):
        response = self.client.get(reverse('diary:diary_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Прогулка')

    def test_diary_detail(self):
        response = self.client.get(reverse('diary:diary_detail', args=[self.entry.pk]))
        self.assertEqual(response.status_code, 200)

    def test_diary_create(self):
        response = self.client.post(
            reverse('diary:diary_create'),
            data={'pet': self.pet.pk, 'date': '2026-11-05', 'title': 'Заметка', 'category': 'health'},
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(DiaryEntry.objects.filter(title='Заметка').exists())

    def test_diary_delete(self):
        response = self.client.post(reverse('diary:diary_delete', args=[self.entry.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(DiaryEntry.objects.filter(pk=self.entry.pk).exists())
