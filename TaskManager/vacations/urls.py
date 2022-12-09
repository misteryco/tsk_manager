from django.urls import path, include

from TaskManager.vacations.views import VacationCreateView, VacationsListView, CalendarView, VacationDetailsView, \
    vacation_edit_view, vacation_approve_disapprove, VacationDelete, vacation_delete

urlpatterns = [
    path('', VacationsListView.as_view(), name='vacations list'),
    path('create/', VacationCreateView.as_view(), name='vacation create'),
    path('calendar/', CalendarView.as_view(), name='vacations calendar'),
    path('<int:pk>/', include([
        path('details/', VacationDetailsView.as_view(), name='vacation details'),
        path('edit/', vacation_edit_view, name='vacation edit'),
        path('delete/', vacation_delete, name='vacation delete'),
        path('change_status/', vacation_approve_disapprove, name='vacation approve'),
        path('change_status/', vacation_approve_disapprove, name='vacation approve'),
    ])),
]
