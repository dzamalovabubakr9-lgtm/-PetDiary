from django.db import models


class AdviceCategory(models.Model):
    """Категория советов по уходу."""
    name = models.CharField(max_length=100, unique=True, verbose_name='Название категории')
    description = models.TextField(blank=True, default='', verbose_name='Описание категории')

    class Meta:
        verbose_name = 'Категория советов'
        verbose_name_plural = 'Категории советов'

    def __str__(self):
        return self.name


class Advice(models.Model):
    """Совет по уходу за питомцем (информационный материал)."""
    category = models.ForeignKey(
        AdviceCategory, on_delete=models.CASCADE, related_name='advice_items', verbose_name='Категория'
    )
    title = models.CharField(max_length=200, verbose_name='Заголовок')
    content = models.TextField(verbose_name='Материал')
    is_published = models.BooleanField(default=True, verbose_name='Опубликован')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    class Meta:
        verbose_name = 'Совет по уходу'
        verbose_name_plural = 'Советы по уходу'
        ordering = ['title']

    def __str__(self):
        return self.title
