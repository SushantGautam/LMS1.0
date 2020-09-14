from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView, ListView, UpdateView, DeleteView

from WebApp.models import MemberInfo
from event_calendar.forms import CalendarEventForm, CalendarEventUpdateForm
from event_calendar.models import CalendarEvent


class EventCreateView(CreateView):
    model = CalendarEvent
    # template_name = 'event_calendar/2.html'
    form_class = CalendarEventForm
    # success_url = reverse_lazy('event_calendar')

    def form_invalid(self, form):
        print(form.errors)
        raise Exception
        return super().form_invalid(form)

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.register_agent = self.request.user
        self.object.save()
        if self.request.GET.get("return", None) == "json":
            response = {'pk': self.object.pk,
                        'part': self.object.get_participation_type_display(),
                        'type': self.object.get_event_type_display(),
                        }
            return JsonResponse(response)
        else:
            return super().form_valid(form)


class EventUpdateView(UpdateView):
    model = CalendarEvent
    # template_name = 'event_calendar/2.html'
    form_class = CalendarEventUpdateForm
    # success_url = reverse_lazy('event_calendar')

    def form_invalid(self, form):
        print(form.errors)
        raise Exception
        return super().form_invalid(form)


class EventListView(ListView):
    model = CalendarEvent
    template_name = "event_calendar/2.html"

    def get_context_data(self):
        context = super().get_context_data()
        users = MemberInfo.objects.filter(Center_Code=self.request.user.Center_Code)
        context['user_list'] = users

        # context['teacher_list'] = users.filter(Is_Teacher=True)
        # context['student_list'] = users.filter(Is_Student=True)
        return context


class EventDeleteView(DeleteView):
    model = CalendarEvent
    form_class = CalendarEventUpdateForm
    # template_name = 'event_calendar/2.html'
    # success_url = reverse_lazy('event_calendar')


class EventUpdatedView(UpdateView):
    model = CalendarEvent
    # template_name = 'event_calendar/2.html'
    form_class = CalendarEventForm
    # success_url = reverse_lazy('event_calendar')

    def form_invalid(self, form):
        print(form.errors)
        raise Exception
        return super().form_invalid(form)
