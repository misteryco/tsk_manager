from datetime import date, timedelta

from django.contrib import admin

from TaskManager.common.models import ShortNewsArticle, NewsComment
from django.utils.translation import gettext_lazy


class WeekSendArticleFilter(admin.SimpleListFilter):
    # Human-readable title which will be displayed in the
    # right admin sidebar just above the filter options.
    title = gettext_lazy('time created')

    # Parameter for the filter that will be used in the URL query.
    parameter_name = 'week'

    def lookups(self, request, model_admin):
        return (
            ('last_15_days', gettext_lazy('in the last 15 days')),
            ('previous_15_days', gettext_lazy('in the previous 15 days')),
            ('earlier', gettext_lazy('earlier')),
        )

    def queryset(self, request, queryset):
        if self.value() == 'last_15_days':
            previous_date = date.today() - timedelta(days=15)
            return queryset.filter(
                date_and_time__gte=previous_date,
                date_and_time__lte=date.today(),
            )
        if self.value() == 'previous_15_days':
            first_date = date.today() - timedelta(days=30)
            second_date = date.today() - timedelta(days=16)
            return queryset.filter(
                date_and_time__gte=first_date,
                date_and_time__lte=second_date,
            )
        if self.value() == 'earlier':
            first_date = date.today() - timedelta(days=31)
            return queryset.filter(
                date_and_time__lte=first_date,
            )


@admin.register(ShortNewsArticle)
class ShortNewsAdmin(admin.ModelAdmin):
    list_display = ('news_Title', 'date_and_time', 'user',)
    list_filter = (WeekSendArticleFilter,)


@admin.register(NewsComment)
class NewsCommentAdmin(admin.ModelAdmin):
    list_display = ('commented_section', 'date_and_time', 'comment_user',)
    list_filter = (WeekSendArticleFilter,)
