from datetime import date, timedelta

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from care.models import Procedure
from pets.models import Pet

User = get_user_model()


class ProcedureTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('careuser', password='SecurePass123!')
        self.pet = Pet.objects.create(owner=self.user, name='Рекс')
        self.client.force_login(self.user)

    def test_procedure_create(self):
        scheduled = (date.today() + timedelta(days=10)).isoformat()
        response = self.client.post(
            reverse('care:procedure_create'),
            data={'pet': self.pet.pk, 'name': 'vaccination', 'scheduled_date': scheduled,
                  'description': 'Первая вакцинация'},
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Procedure.objects.filter(pet=self.pet, name='vaccination').exists())

    def test_procedures_list(self):
        Procedure.objects.create(pet=self.pet, name='bath', scheduled_date=date(2026, 12, 1))
        response = self.client.get(reverse('care:procedures'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Купание')

    def test_procedure_update_done(self):
        proc = Procedure.objects.create(pet=self.pet, name='nail_trim', scheduled_date=date(2026, 11, 10))
        response = self.client.post(
            reverse('care:procedure_edit', args=[proc.pk]),
            data={'pet': self.pet.pk, 'name': 'nail_trim', 'scheduled_date': '2026-11-10', 'done': 'on'},
        )
        self.assertEqual(response.status_code, 302)
        proc.refresh_from_db()
        self.assertTrue(proc.done)
