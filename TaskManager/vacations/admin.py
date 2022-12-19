from django.contrib import admin

from TaskManager.vacations.models import Vacation


@admin.register(Vacation)
class Vacation(admin.ModelAdmin):
    list_display = ('user', 'approved', 'start_date', 'end_date',)
    list_filter = ('approved',)

    def get_ordering(self, request):
        return ['start_date', ]
