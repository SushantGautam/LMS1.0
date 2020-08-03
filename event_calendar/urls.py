from django.urls import path

from event_calendar import views

urlpatterns = (
    # path('', views.CalendarIndex.as_view(), name='event_calendar'),
    path('create', views.EventCreateView.as_view(), name='event_calendar_create'),
    path('', views.EventListView.as_view(), name='event_calendar'),
)




