from django.shortcuts import render

# Create your views here.
from django.views.generic import TemplateView


class CalendarIndex(TemplateView):
    template_name = 'event_calendar/index.html'
