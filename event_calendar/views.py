from django.shortcuts import render

# Create your views here.
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView, ListView

from event_calendar.forms import CalendarEventForm
from event_calendar.models import CalendarEvent


class CalendarIndex(TemplateView):
    template_name = 'event_calendar/index.html'

    def get_context_data(self):
        context = super().get_context_data()
        context['form'] = CalendarEventForm()
        return context


class EventCreateView(CreateView):
    model = CalendarEvent
    template_name = 'event_calendar/index.html'
    form_class = CalendarEventForm
    success_url = reverse_lazy('event_calendar')

    def form_invalid(self, form):
        print(form.errors)
        return super().form_invalid(form)

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.register_agent = self.request.user
        return super().form_valid(form)


class EventListView(ListView):
    model = CalendarEvent
    template_name = "event_calendar/index.html"





