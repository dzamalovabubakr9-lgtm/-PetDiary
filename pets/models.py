from django.db import models

from accounts.models import User


class Pet(models.Model):
    """Карточка питомца."""

    SPECIES_CHOICES = [
        ('dog', 'Собака'),
        ('cat', 'Кошка'),
        ('bird', 'Птица'),
        ('rabbit', 'Кролик'),
        ('hamster', 'Хомяк'),
        ('mouse', 'Мышь'),
        ('ferret', 'Фрит'),
        ('guinea_pig', 'Морская свинка'),
        ('other', 'Другое'),
    ]
    SEX_CHOICES = [
        ('male', 'Самец'),
        ('female', 'Самка'),
        ('unknown', 'Не указано'),
    ]

    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='pets', verbose_name='Владелец')
    name = models.CharField(max_length=100, verbose_name='Кличка')
    species = models.CharField(max_length=20, choices=SPECIES_CHOICES, default='other', verbose_name='Вид животного')
    breed = models.CharField(max_length=100, blank=True, default='', verbose_name='Порода')
    sex = models.CharField(max_length=10, choices=SEX_CHOICES, default='unknown', verbose_name='Пол')
    birth_date = models.DateField(null=True, blank=True, verbose_name='Дата рождения')
    weight = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, verbose_name='Вес (кг)')
    photo = models.ImageField(upload_to='pets/photos/', blank=True, null=True, verbose_name='Фото')
    description = models.TextField(blank=True, default='', verbose_name='Описание')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания записи')

    class Meta:
        verbose_name = 'Питомец'
        verbose_name_plural = 'Питомцы'
        ordering = ['name']

    def __str__(self):
        return f'{self.name} ({self.get_species_display()})'


class Measurement(models.Model):
    """Измерение показателей питомца (вес, размер и т.д.)."""

    pet = models.ForeignKey(Pet, on_delete=models.CASCADE, related_name='measurements', verbose_name='Питомец')
    weight = models.DecimalField(max_digits=6, decimal_places=2, verbose_name='Вес (кг)')
    measurement_date = models.DateField(verbose_name='Дата измерения')
    note = models.TextField(blank=True, default='', verbose_name='Примечание')

    class Meta:
        verbose_name = 'Измерение'
        verbose_name_plural = 'Измерения'
        ordering = ['-measurement_date']
