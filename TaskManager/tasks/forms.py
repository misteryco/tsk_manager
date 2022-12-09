from django.forms import ModelForm, Form, DateInput
from django import forms

from TaskManager.tasks.models import Task


# Create custom widget in your forms.py file.

class TasksCreateForm(ModelForm):
    class Meta:
        model = Task
        exclude = ('user', 'attached_file_by_executor')
        widgets = {
            'due_date': DateInput(attrs={'placeholder': 'mm/dd/yyyy', 'type-date': 'date', }),
        }


class TaskSearchForm(Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['search_in_task_name_or_description'].label = ''

    MAX_SEARCH_LEN = 100

    search_in_task_name_or_description = forms.CharField(
        max_length=MAX_SEARCH_LEN,
        required=False,
    )
