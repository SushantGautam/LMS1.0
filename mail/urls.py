from django.urls import path
from mail.views import MailListView, MailDetailView, ReplyCreateView, MailMultipleCreate, MailSendDraftListView, \
    SendDetailView, DraftUpdateView, DraftCreateView, MailDeleteView, MailReceiverDeleteView, StarView, TrashView, \
    mail_spam, mail_starred, sender_starred, mail_deleted, sender_delete, mail_send, mail_viewed, mail_unread

from mail import views

urlpatterns = (
    # path('', views.MailList, name='inbox_list'),
    path('', MailListView.as_view(), name='mail_list'),
    path('mail_outbox', MailSendDraftListView.as_view(), name='mail_send_list'),
    path('mail_starred', StarView.as_view(), name='star_list'),
    path('mail_trashed', TrashView.as_view(), name='trash_list'),

    path('mail_detail/<int:pk>', MailDetailView.as_view(), name='mail_detail'),
    path('send_detail/<int:pk>', SendDetailView.as_view(), name='send_detail'),
    path('draft_create', DraftCreateView.as_view(), name='draft_create'),
    path('mail_draft_detail/<int:pk>', DraftUpdateView.as_view(), name='mail_draft_detail'),
    path('mail_delete/<int:pk>', MailDeleteView, name='mail_delete'),
    path('mail_receiver_delete/<int:pk>', MailReceiverDeleteView.as_view(), name='mail_receiver_delete'),
    path('mail_create', MailMultipleCreate.as_view(), name='mail_create'),
    path('reply_create', ReplyCreateView.as_view(), name='reply_create'),
    path('mail_spam/<int:pk>', mail_spam, name='mail_spam'),
    path('mail_starred/<int:pk>', mail_starred, name='mail_starred'),
    path('sender_starred/<int:pk>', sender_starred, name='sender_starred'),
    path('mail_deleted/<int:pk>', mail_deleted, name='mail_deleted'),
    path('sender_delete/<int:pk>', sender_delete, name='sender_delete'),
    path('mail_send/<int:pk>', mail_send, name='mail_send'),
    path('mail_viewed/<int:pk>', mail_viewed, name='mail_viewed'),
    path('mail_unread/<int:pk>', mail_unread, name='mail_unread'),
)