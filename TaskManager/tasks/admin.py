from datetime import date, timedelta

from django.contrib import admin
from django.db.models.functions import Lower
from django.utils.translation import gettext_lazy

from TaskManager.tasks.models import Task


class WeekSendArticleFilter(admin.SimpleListFilter):
    # Human-readable title which will be displayed in the
    # right admin sidebar just above the filter options.
    title = gettext_lazy('Task with Due Date for Task:')

    # Parameter for the filter that will be used in the URL query.
    parameter_name = 'week'

    def lookups(self, request, model_admin):
        return (
            ('last_15_days', gettext_lazy('In the previous 15 days.')),
            ('next_15_days', gettext_lazy('In the next 15 days.')),
            ('later', gettext_lazy('After more than 15 days.')),
        )

    def queryset(self, request, queryset):
        if self.value() == 'last_15_days':
            previous_date = date.today() - timedelta(days=15)
            return queryset.filter(
                due_date__gte=previous_date,
                due_date__lte=date.today(),
            )
        if self.value() == 'next_15_days':
            first_date = date.today()
            second_date = date.today() + timedelta(days=15)
            return queryset.filter(
                due_date__gte=first_date,
                due_date__lte=second_date,
            )
        if self.value() == 'later':
            first_date = date.today() - timedelta(days=16)
            return queryset.filter(
                due_date__lte=first_date,
            )


@admin.register(Task)
class Task(admin.ModelAdmin):
    list_display = ('name', 'user', 'due_date', 'files_attached')
    ordering = ('due_date', 'name', 'user',)
    list_filter = (WeekSendArticleFilter,)

    def files_attached(self, obj):
        if obj.attached_file_by_executor or obj.attached_file_by_author:
            return True

    files_attached.short_description = 'any files attached'

    def get_ordering(self, request):
        # sort case-insensitive
        return [Lower('name')]
    # TODO : Custom Filter
