from django.urls import path, include

from TaskManager.tasks.views import TasksCreateView, TaskDetailsView, TaskEditView, task_list_funct_view, TasksListView

urlpatterns = [
    path('other/', TasksListView.as_view(), name='tasks list'),
    path('', task_list_funct_view, name='tasks list'),
    path('create/', TasksCreateView.as_view(), name='task create'),
    path('<int:pk>/', include([
        path('details/', TaskDetailsView.as_view(), name='task detail'),
        path('edit/', TaskEditView.as_view(), name='task edit'),
    ])),
]
