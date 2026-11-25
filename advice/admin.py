from django.contrib import admin

from advice.models import Advice, AdviceCategory


@admin.register(AdviceCategory)
class AdviceCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)


@admin.register(Advice)
class AdviceAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'is_published', 'created')
    list_filter = ('category', 'is_published')
    search_fields = ('title', 'content')
