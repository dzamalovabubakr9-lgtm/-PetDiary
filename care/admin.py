from django.contrib import admin

from care.models import Procedure, ProcedureLog


@admin.register(Procedure)
class ProcedureAdmin(admin.ModelAdmin):
    list_display = ('pet', 'name', 'scheduled_date', 'done', 'done_at')
    list_filter = ('name', 'done')
    search_fields = ('pet__name', 'description')


@admin.register(ProcedureLog)
class ProcedureLogAdmin(admin.ModelAdmin):
    list_display = ('pet', 'name', 'done_date', 'comment')
    list_filter = ('name',)
    search_fields = ('pet__name', 'name')
