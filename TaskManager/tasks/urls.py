from django.urls import path, include

from TaskManager.tasks.views import TasksCreateView, TaskDetailsView, TaskEditView, task_list_funct_view, \
    task_delete, task_create_view

urlpatterns = [
    path('', task_list_funct_view, name='tasks list'),
    path('create/', TasksCreateView.as_view(), name='task create'),
    path('create2/', task_create_view, name='task create2'),
    path('<int:pk>/', include([
        path('details/', TaskDetailsView.as_view(), name='task detail'),
        path('edit/', TaskEditView.as_view(), name='task edit'),
        path('delete/', task_delete, name='task delete'),
    ])),
]
