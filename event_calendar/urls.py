from django.urls import path

from event_calendar import views

urlpatterns = (
    path('create', views.EventCreateView.as_view(), name='event_calendar_create'),
    path('update/<int:pk>', views.EventUpdateView.as_view(), name='event_calendar_update'),
    path('', views.EventListView.as_view(), name='event_calendar'),
)




