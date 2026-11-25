from django.test import TestCase
from django.urls import reverse

from advice.models import Advice, AdviceCategory


class AdviceTests(TestCase):
    def setUp(self):
        self.cat = AdviceCategory.objects.create(name='Питание', description='Советы по питанию')
        Advice.objects.create(
            category=self.cat, title='Кормление собак',
            content='Давайте корм раз в день, вода всегда свежая.',
        )

    def test_advice_list(self):
        response = self.client.get(reverse('advice:advice_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Кормление собак')

    def test_advice_detail(self):
        advice = Advice.objects.first()
        response = self.client.get(reverse('advice:advice_detail', args=[advice.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, advice.title)

    def test_unpublished_not_shown(self):
        advice = Advice.objects.first()
        advice.is_published = False
        advice.save()
        response = self.client.get(reverse('advice:advice_list'))
        self.assertNotContains(response, advice.title)
