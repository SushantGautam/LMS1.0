from django.urls import path

from event_calendar import views

urlpatterns = (
    path('', views.CalendarIndex.as_view(), name='event_calendar'),
)