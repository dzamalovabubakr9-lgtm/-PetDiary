from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Расширенный пользователь системы с явной ролью RBAC."""
    ROLE_CHOICES = [('user', 'Пользователь'), ('admin', 'Администратор')]
    email = models.EmailField(unique=True, verbose_name='Электронная почта')
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='user', db_index=True)
    phone = models.CharField(max_length=20, blank=True, default='', verbose_name='Телефон')
    groups = models.ManyToManyField(
        'auth.Group', blank=True, related_name='accounts_users', verbose_name='Группы'
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission', blank=True, related_name='accounts_users', verbose_name='Права пользователя'
    )


class Role(models.Model):
    """Роль пользователя (уровень доступа)."""
    name = models.CharField(max_length=50, unique=True, verbose_name='Название роли')
    description = models.TextField(blank=True, verbose_name='Описание роли')

    class Meta:
        verbose_name = 'Роль'
        verbose_name_plural = 'Роли'

    def __str__(self):
        return self.name


class Profile(models.Model):
    """Расширенный профиль пользователя."""
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='profile', verbose_name='Пользователь'
    )
    avatar = models.ImageField(
        upload_to='avatars/', blank=True, null=True, verbose_name='Аватар'
    )
    birthday = models.DateField(blank=True, null=True, verbose_name='Дата рождения')
    about = models.TextField(blank=True, default='', verbose_name='О себе')
    phone = models.CharField(max_length=20, blank=True, default='', verbose_name='Телефон')
    role = models.ForeignKey(
        Role, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Роль'
    )

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'

    def __str__(self):
        return f'{self.user.username} — {self.role.name if self.role else "нет роли"}'
