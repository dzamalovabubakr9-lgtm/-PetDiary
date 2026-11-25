from django.db import models

from pets.models import Pet


class Procedure(models.Model):
    """Планируемая процедура (вакцинация, купание и т.д.)."""

    PROCEDURE_CHOICES = [
        ('vaccination', 'Вакцинация'),
        ('parasite_treatment', 'Обработка от паразитов'),
        ('deworming', 'Дегельминтизация'),
        ('bath', 'Купание'),
        ('nail_trim', 'Стрижка когтей'),
        ('dental_cleaning', 'Чистка зубов'),
        ('preventive_check', 'Профилактический осмотр'),
        ('vet_visit', 'Посещение ветеринара'),
    ]

    pet = models.ForeignKey(Pet, on_delete=models.CASCADE, related_name='procedures', verbose_name='Питомец')
    name = models.CharField(max_length=30, choices=PROCEDURE_CHOICES, verbose_name='Название процедуры')
    description = models.TextField(blank=True, default='', verbose_name='Описание процедуры')
    scheduled_date = models.DateField(verbose_name='Дата запланированной процедуры')
    done = models.BooleanField(default=False, verbose_name='Выполнена')
    done_at = models.DateField(null=True, blank=True, verbose_name='Дата выполнения')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    class Meta:
        verbose_name = 'Процедура'
        verbose_name_plural = 'Процедуры'
        ordering = ['-scheduled_date']

    def __str__(self):
        return f'{self.get_name_display()} — {self.pet.name} ({self.scheduled_date})'


class ProcedureLog(models.Model):
    """Запись о выполненной процедуре (история)."""

    pet = models.ForeignKey(Pet, on_delete=models.CASCADE, related_name='procedure_logs', verbose_name='Питомец')
    procedure = models.ForeignKey(
        Procedure, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Процедура'
    )
    name = models.CharField(max_length=30, choices=Procedure.PROCEDURE_CHOICES, verbose_name='Название')
    done_date = models.DateField(verbose_name='Дата выполнения')
    comment = models.TextField(blank=True, default='', verbose_name='Примечание')

    class Meta:
        verbose_name = 'Запись о процедуре'
        verbose_name_plural = 'Записи о процедурах'
        ordering = ['-done_date']

    def __str__(self):
        return f'{self.pet.name} — {self.get_name_display()} ({self.done_date})'
