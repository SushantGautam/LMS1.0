from django.urls import path

from mail import views

urlpatterns = (
    path('', views.MailList, name='inbox_list'),
)