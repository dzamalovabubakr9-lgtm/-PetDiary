from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from accounts.models import Profile, Role, User


class ProfileInline(admin.StackedInline):
    model = Profile
    extra = 0
    can_delete = False


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'phone', 'is_staff', 'is_active')
    search_fields = ('username', 'email')
    inlines = (ProfileInline,)


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone', 'role', 'birthday')
    search_fields = ('user__username', 'user__email')
