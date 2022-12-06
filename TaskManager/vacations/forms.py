from django.forms import ModelForm, DateInput
# from django import forms

from TaskManager.vacations.models import Vacation


class VacationBaseForm(ModelForm):
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     for field_name, field_object in self.fields.items():
    #         field_object.widget.attrs['disabled'] = 'disabled'
    #         field_object.required = False
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # input_formats to parse HTML5 datetime-local input to datetime field
        # self.fields['start_date'].input_formats = ('%Y-%m-%d',)
        # self.fields['end_date'].input_formats = ('%Y-%m-%d',)

    class Meta:
        model = Vacation
        exclude = ('user',)
        widgets = {
            # 'start_date': DateInput(attrs={'type': 'date'}),
            'start_date': DateInput(attrs={'placeholder': 'mm/dd/yyyy', 'type': 'date', }),
            # 'end_date': DateInput(attrs={'type': 'date'}),
            'end_date': DateInput(attrs={'placeholder': 'mm/dd/yyyy', 'type': 'date', }),
        }


class VacationCreateForm(VacationBaseForm):
    pass


class VacationEditForm(VacationBaseForm):
    pass
    # class Meta:
    #     exclude = ('approved',)


class VacationEditForTeamLead(VacationBaseForm):
    class Meta:
        fields = '__all__'
