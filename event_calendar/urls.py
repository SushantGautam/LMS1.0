from django.urls import path

from event_calendar import views

urlpatterns = (
    path('create', views.EventCreateView.as_view(), name='event_calendar_create'),
    path('update/<int:pk>', views.EventUpdateView.as_view(), name='event_calendar_update'),
    path('updated/<int:pk>', views.EventUpdatedView.as_view(), name='event_calendar_updated'),
    path('delete/<int:pk>', views.EventDeleteView.as_view(), name='event_calendar_delete'),
    path('', views.EventListView.as_view(), name='event_calendar'),
)




