from django.urls import path, include

from TaskManager.vacations.views import VacationCreateView, VacationsListView, CalendarView, VacationDetailsView, \
    VacationEditView, vacation_edit_view, vacation_approve_disapprove

urlpatterns = [
    path('', VacationsListView.as_view(), name='vacations list'),
    path('create/', VacationCreateView.as_view(), name='vacation create'),
    path('calendar/', CalendarView.as_view(), name='vacations calendar'),
    path('<int:pk>/', include([
        path('details/', VacationDetailsView.as_view(), name='vacation details'),
        # path('edit/', VacationEditView.as_view(), name='vacation edit'),
        path('edit/', vacation_edit_view, name='vacation edit'),
        path('change_status/', vacation_approve_disapprove, name='vacation approve'),

    ])),
]
