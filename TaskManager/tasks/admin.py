from django.contrib import admin
from django.db.models.functions import Lower

from TaskManager.tasks.models import Task


@admin.register(Task)
class Task(admin.ModelAdmin):
    list_display = ('name', 'user', 'due_date', 'files_attached')
    ordering = ('due_date', 'name', 'user',)

    def files_attached(self, obj):
        if obj.attached_file_by_executor or obj.attached_file_by_author:
            return True

    files_attached.short_description = 'any files attached'

    def get_ordering(self, request):
        # sort case-insensitive
        return [Lower('name')]
