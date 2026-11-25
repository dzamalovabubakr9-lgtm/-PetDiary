from django.contrib import admin

from pets.models import Measurement, Pet


@admin.register(Pet)
class PetAdmin(admin.ModelAdmin):
    list_display = ('name', 'species', 'breed', 'owner', 'birth_date', 'weight', 'sex')
    list_filter = ('species', 'sex')
    search_fields = ('name', 'owner__username')


@admin.register(Measurement)
class MeasurementAdmin(admin.ModelAdmin):
    list_display = ('pet', 'weight', 'measurement_date', 'note')
    list_filter = ('pet',)
    search_fields = ('pet__name',)
