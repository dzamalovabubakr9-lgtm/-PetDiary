from django.contrib import admin

from diary.models import DiaryEntry, VetVisit


@admin.register(DiaryEntry)
class DiaryEntryAdmin(admin.ModelAdmin):
    list_display = ('date', 'title', 'pet', 'category', 'created')
    list_filter = ('category', 'date')
    search_fields = ('title', 'pet__name')
    list_select_related = ('pet',)


@admin.register(VetVisit)
class VetVisitAdmin(admin.ModelAdmin):
    list_display = ('pet', 'date', 'description')
    search_fields = ('pet__name', 'description')
