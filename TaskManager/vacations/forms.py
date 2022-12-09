from django.forms import ModelForm, DateInput
# from django import forms

from TaskManager.vacations.models import Vacation


class VacationBaseForm(ModelForm):
    class Meta:
        model = Vacation
        exclude = ('user',)
        widgets = {
            'start_date': DateInput(attrs={'placeholder': 'mm/dd/yyyy', 'type': 'date', }),
            'end_date': DateInput(attrs={'placeholder': 'mm/dd/yyyy', 'type': 'date', }),
        }


class VacationCreateForm(VacationBaseForm):
    class Meta:
        model = Vacation
        exclude = ('user', 'approved')


class VacationEditForm(VacationBaseForm):
    def __int__(self, *args, **kwargs):
        for field_name, field_object in self.fields.items():
            # if field_name in ('approved',):
            field_object.widget.attrs['disabled'] = 'disabled'

    class Meta:
        model = Vacation
        exclude = ('user', 'approved')