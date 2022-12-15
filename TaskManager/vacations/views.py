import calendar
from datetime import date, datetime, timedelta

from django.contrib.auth import mixins as auth_mixins
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.utils.safestring import mark_safe
from django.views import generic as views

from TaskManager.core.utils import Calendar
from TaskManager.vacations.forms import VacationCreateForm, VacationEditForm
from TaskManager.vacations.models import Vacation


def get_date(req_day):
    if req_day:
        year, month = (int(x) for x in req_day.split('-'))
        return date(year, month, day=1)
    return datetime.today()


def prev_month(d):
    first = d.replace(day=1)
    prev_month = first - timedelta(days=1)
    month = 'month=' + str(prev_month.year) + '-' + str(prev_month.month)
    return month


def next_month(d):
    days_in_month = calendar.monthrange(d.year, d.month)[1]
    last = d.replace(day=days_in_month)
    next_month = last + timedelta(days=1)
    month = 'month=' + str(next_month.year) + '-' + str(next_month.month)
    return month


class VacationCreateView(auth_mixins.LoginRequiredMixin, views.CreateView):
    template_name = 'vacations/../../templates/base/base-create-view.html'
    form_class = VacationCreateForm

    success_url = reverse_lazy('vacations list')

    def form_valid(self, form):
        vacation = form.save(commit=False)
        vacation.user = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_title'] = 'Create Vacation'
        context['form__button_title'] = 'CREATE'
        return context


class VacationsListView(LoginRequiredMixin, views.ListView):
    model = Vacation
    template_name = 'vacations/vacations_list.html'
    context_object_name = 'vacations'

    def get_context_data(self, *args, **kwargs):
        total_vacations = self.model.objects.count()
        waiting_approval_vacations = self.model.objects.filter(approved=False)

        context = super().get_context_data(*args, **kwargs)
        context['total_vacations'] = total_vacations
        context['waiting_approval_vacations'] = waiting_approval_vacations

        return context


class CalendarView(LoginRequiredMixin, views.ListView):
    model = Vacation
    template_name = 'vacations/vacations_calendar.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # use today's date for the calendar
        d = get_date(self.request.GET.get('month', None))
        # Instantiate our calendar class with today's year and date
        cal = Calendar(d.year, d.month)
        # Call the formatmonth method, which returns our calendar as a table
        html_cal = cal.formatmonth(withyear=True)
        context['calendar'] = mark_safe(html_cal)
        context['prev_month'] = prev_month(d)
        context['next_month'] = next_month(d)
        # context['user'] = self.request.user
        return context


class VacationDetailsView(LoginRequiredMixin, views.DetailView):
    template_name = 'vacations/vacation-details.html'
    model = Vacation


@login_required
def vacation_edit_view(request, pk):
    vacation = Vacation.objects.filter(pk=pk).get()
    if request.method == 'POST':
        form = VacationEditForm(request.POST)
        if form.is_valid():
            new_start_date = form.cleaned_data['start_date']
            new_end_date = form.cleaned_data['end_date']
            if new_start_date != vacation.start_date or new_end_date != vacation.end_date:
                vacation.start_date = new_start_date
                vacation.end_date = new_end_date
                vacation.approved = 0
                vacation.save()
            return redirect('vacation details', pk=pk)
    else:
        form = VacationEditForm(instance=vacation)

    context = {
        'form': form,
        'vacation': vacation,
    }
    return render(request, template_name='vacations/vacation-edit.html', context=context)


@login_required
def vacation_approve_disapprove(request, pk):
    # TODO: Exception
    vacation = Vacation.objects.filter(pk=pk).get()

    if request.user.level != 'team_lead':
        raise PermissionDenied()

    if not vacation.approved:
        vacation.approved = True
    else:
        vacation.approved = False
    vacation.save()
    return redirect('vacations list')


@login_required
def vacation_delete(request, pk):
    # TODO: Exception
    vacation = Vacation.objects.filter(pk=pk).get()
    if request.user != vacation.user:
        raise PermissionDenied()
    vacation.delete()
    return redirect('vacations list')
