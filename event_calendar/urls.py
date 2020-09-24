from django.urls import path, reverse_lazy

from event_calendar import views

urlpatterns = (
    path('create', views.EventCreateView.as_view(template_name='event_calendar/index.html',
                                                 success_url=reverse_lazy('event_calendar')),
         name='event_calendar_create'),
    path('update/<int:pk>', views.EventUpdateView.as_view(template_name='event_calendar/index.html',
                                                          success_url=reverse_lazy('event_calendar')),
         name='event_calendar_update'),
    path('updated/<int:pk>', views.EventUpdatedView.as_view(template_name='event_calendar/index.html',
                                                            success_url=reverse_lazy('event_calendar')),
         name='event_calendar_updated'),
    path('delete/<int:pk>', views.EventDeleteView.as_view(template_name='event_calendar/index.html',
                                                          success_url=reverse_lazy('event_calendar')),
         name='event_calendar_delete'),
    path('', views.EventListView.as_view(template_name='event_calendar/index.html'), name='event_calendar'),
)
