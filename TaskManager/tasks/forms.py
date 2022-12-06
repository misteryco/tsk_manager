from django.forms import ModelForm, Form
from django import forms

from TaskManager.tasks.models import Task


class TasksCreateForm(ModelForm):
    class Meta:
        model = Task
        exclude = ('user', 'attached_file_by_executor')


class TaskSearchForm(Form):
    MAX_SEARCH_LEN = 100

    search_in_task_name = forms.CharField(max_length=MAX_SEARCH_LEN, required=False)
