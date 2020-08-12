from django.forms import ModelForm, DateTimeField, DateTimeInput

from event_calendar.models import CalendarEvent


class CalendarEventForm(ModelForm):
    class Meta:
        model = CalendarEvent
        fields = ['title', 'event_type', 'date_start', 'date_end', 'description', 'participants', 'is_all_day']


class CalendarEventUpdateForm(ModelForm):
    class Meta:
        model = CalendarEvent
        fields = ['date_start', 'date_end']








