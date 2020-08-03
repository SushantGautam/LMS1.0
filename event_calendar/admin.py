from django.contrib import admin
from event_calendar import models
from django import forms


class EventCalendarAdminForm(forms.ModelForm):
    class Meta:
        model = models.CalendarEvent
        exclude = []


class EventCalendarAdmin(admin.ModelAdmin):
    form = EventCalendarAdminForm

    def start_time(self, obj):
        return obj.date_start.strftime("%d %b %Y %H:%M:%S")

    def end_time(self, obj):
        return obj.date_end.strftime("%d %b %Y %H:%M:%S")

    start_time.admin_order_field = 'date_start'
    start_time.short_description = 'Start Date'
    end_time.admin_order_field = 'date_end'
    end_time.short_description = 'End Date'

    list_display = ('pk', 'title', 'event_type', 'start_time', 'end_time', 'register_agent')
    search_fields = ('description', 'register_agent', 'title')


admin.site.register(models.CalendarEvent, EventCalendarAdmin)