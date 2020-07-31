from django.contrib import admin
from event_calendar import models
from django import forms


class EventCalendarAdminForm(forms.ModelForm):
    class Meta:
        model = models.CalendarEvent
        exclude = []


class EventCalendarAdmin(admin.ModelAdmin):
    form = EventCalendarAdminForm
    list_display = ('pk', 'title', 'event_type', 'date_start', 'date_end', 'register_agent')
    search_fields = ('description', 'register_agent', 'title')


admin.site.register(models.CalendarEvent, EventCalendarAdmin)