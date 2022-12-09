from calendar import HTMLCalendar
from datetime import date

from TaskManager.vacations.models import Vacation


class Calendar(HTMLCalendar):
    def __init__(self, year=None, month=None):
        self.year = year
        self.month = month
        super(Calendar, self).__init__()

    # formats a day as a td
    # filter events by date and adds them as li
    def formatday(self, day, month, year, vacations):

        current_date = date(year, month, day) if day != 0 else date(year, month, 1)

        events_per_day = vacations.filter(start_date__lte=current_date, end_date__gte=current_date)
        d = ''

        for event in events_per_day:
            d += f'<li> "{event.user.first_name} {event.user.last_name}" in vacation from {event.start_date} till' \
                 f' {event.end_date} </li>'

        if day != 0:
            return f"<td><span class='date'>{day}</span><ul> {d} </ul></td>"
        return '<td></td>'

    # formats a week as a tr
    def formatweek(self, theweek, month, year, vacations):
        week = ''
        for d, weekday in theweek:
            week += self.formatday(d, month, year, vacations)
        return f'<tr> {week} </tr>'

    # formats a month as a table
    # filter events by year and month
    def formatmonth(self, withyear=True):
        # vacations = Vacation.objects.filter(start_date__year=self.year, start_date__month__lte=self.month,
        #                                     end_date__month__gte=self.month)
        vacations = Vacation.objects.all()
        cal = f'<table border="0" cellpadding="0" cellspacing="0" class="calendar">\n'
        cal += f'{self.formatmonthname(self.year, self.month, withyear=withyear)}\n'
        cal += f'{self.formatweekheader()}\n'
        for week in self.monthdays2calendar(self.year, self.month):
            cal += f'{self.formatweek(week, self.month, self.year, vacations)}\n'
        return cal
