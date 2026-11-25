from django.db import models

from pets.models import Pet


class DiaryEntryCategory(models.TextChoices):
    HEALTH = 'health', 'Здоровье'
    NUTRITION = 'nutrition', 'Питание'
    WALKS = 'walks', 'Прогулки'
    BEHAVIOR = 'behavior', 'Поведение'
    CARE = 'care', 'Уход'
    WEIGHT = 'weight', 'Вес'
    VET_VISIT = 'vet_visit', 'Посещение ветеринара'
    OTHER = 'other', 'Другие события'


class DiaryEntry(models.Model):
    """Дневниковая запись о питомце."""

    pet = models.ForeignKey(Pet, on_delete=models.CASCADE, related_name='diary_entries', verbose_name='Питомец')
    date = models.DateField(verbose_name='Дата записи')
    title = models.CharField(max_length=200, verbose_name='Заголовок')
    description = models.TextField(blank=True, default='', verbose_name='Описание')
    category = models.CharField(
        max_length=20, choices=DiaryEntryCategory.choices, default=DiaryEntryCategory.OTHER,
        verbose_name='Категория',
    )
    created = models.DateTimeField(auto_now_add=True, verbose_name='Время создания записи')

    class Meta:
        verbose_name = 'Дневниковая запись'
        verbose_name_plural = 'Дневниковые записи'
        ordering = ['-date', '-created']

    def __str__(self):
        return f'{self.date}: {self.title}'


class VetVisit(models.Model):
    """Посещение ветеринара."""

    pet = models.ForeignKey(Pet, on_delete=models.CASCADE, related_name='vet_visits', verbose_name='Питомец')
    date = models.DateField(verbose_name='Дата посещения')
    description = models.TextField(blank=True, default='', verbose_name='Описание визита')
    recommendations = models.TextField(blank=True, default='', verbose_name='Рекомендации врача')

    class Meta:
        verbose_name = 'Посещение ветеринара'
        verbose_name_plural = 'Посещения ветеринара'
        ordering = ['-date']

    def __str__(self):
        return f'{self.pet.name} — {self.date}'
