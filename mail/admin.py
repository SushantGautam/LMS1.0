from django.contrib import admin
from mail.models import Mail, MailReceiver

admin.site.register(Mail)
admin.site.register(MailReceiver)
