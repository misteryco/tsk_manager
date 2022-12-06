import calendar
from calendar import HTMLCalendar
from datetime import date, datetime, timedelta

from django.contrib.auth import mixins as auth_mixins
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.template.context_processors import request
from django.urls import reverse_lazy
from django.utils.safestring import mark_safe
from django.views import generic as views

from TaskManager.core.utils import Calendar
from TaskManager.vacations.forms import VacationCreateForm, VacationEditForm, VacationEditForTeamLead
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
    template_name = 'vacations/vacation_create_view.html'
    form_class = VacationCreateForm

    success_url = reverse_lazy('vacations list')

    def form_valid(self, form):
        vacation = form.save(commit=False)
        vacation.user = self.request.user
        return super().form_valid(form)


class VacationsListView(views.ListView):
    model = Vacation
    template_name = 'vacations/vacations_list.html'
    context_object_name = 'vacations'

    def get_context_data(self, *args, **kwargs):
        total_vacations = self.model.objects.count()
        waiting_approval_vacations = self.model.objects.filter(approved=False)
        # waiting_approval_vacations_count = waiting_approval_vacations.count()
        context = super().get_context_data(*args, **kwargs)
        context['total_vacations'] = total_vacations
        context['waiting_approval_vacations'] = waiting_approval_vacations
        # context['waiting_approval_vacations_count'] = waiting_approval_vacations_count

        return context


class CalendarView(views.ListView):
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
        return context


class VacationDetailsView(views.DetailView):
    template_name = 'vacations/vacation-details.html'
    model = Vacation


class VacationEditView(views.UpdateView):
    template_name = 'vacations/vacation-edit.html'
    model = Vacation
    fields = ['start_date', 'end_date', ]

    def get_user_level(self):
        if self.request.user.level == 'team_lead':
            self.fields.append('approved')

    def get_success_url(self):
        return reverse_lazy(
            'vacation details',
            kwargs={'pk': self.object.pk})


@login_required
def vacation_edit_view(request, pk):
    user_level = request.user.level
    vacation = Vacation.objects.filter(pk=pk).get()
    if request.method == 'POST':
        form = VacationEditForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('vacation details')
    else:
        if user_level == 'team_lead':
            form = VacationEditForm(instance=vacation)
        else:
            form = VacationEditForTeamLead(instance=vacation)
    context = {
        "form": form,
    }
    return render(request, template_name='vacations/vacation-edit.html', context=context)


def vacation_approve_disapprove(request, pk):
    vacation = Vacation.objects.filter(pk=pk).get()
    if not vacation.approved:
        vacation.approved = True
    else:
        vacation.approved = False
    vacation.save()
    return redirect('vacations list')
