import os

from django.db import models
from django.dispatch import receiver

from WebApp.models import MemberInfo


def file_name(instance, filename):
    return 'mail/user_{0}/{1}'.format(instance.sender.id, filename)


class Mail(models.Model):
    receiver_list = models.CharField(max_length=1000, blank=True, null=True)
    LABEL_CHOICES = (('GR', 'General'), ('SP', 'Support'), ('AS', 'Assignment'), ('EX', 'Examination'),
                     ('PR', 'Practical'))
    subject = models.CharField(max_length=100, blank=True, null=True)
    label = models.CharField(max_length=2, choices=LABEL_CHOICES, default='GR')
    body = models.TextField(blank=True, null=True)
    attachment = models.FileField(upload_to=file_name, blank=True, null=True)
    created_date = models.DateTimeField(auto_now_add=True)
    sender_starred = models.BooleanField(default=False)
    sender_delete = models.BooleanField(default=False)
    sender_delete_p = models.BooleanField(default=False)
    is_mail = models.BooleanField(default=True)
    mail_draft = models.BooleanField(default=False)
    # related fields
    sender = models.ForeignKey(MemberInfo, on_delete=models.DO_NOTHING, related_name="mail_sender")
    reply_to = models.ForeignKey("self", blank=True, null=True, on_delete=models.CASCADE)

    def can_delete(self):
        if self.mailreceiver_set.exists():
            return False
        else:
            return True

    def save(self, *args, **kwargs):
        self.is_mail = True
        super().save(*args, **kwargs)

    def __str__(self):
        return self.subject
        # + '--' + self.sender.username

    def get_file_upload_name(self):
        if self.attachment:
            return os.path.split(self.attachment.name)[1]
        else:
            return ""

    def get_receiver_list(self):
        print("receivers:", self.receiver_list)

        receiver_list = self.receiver_list
        if len(receiver_list):
            print("a")
            r_list = receiver_list.split(',')
            print("b")
            print(r_list)
            return [int (r) for r in r_list]



class MailReceiver(models.Model):
    received_date = models.DateTimeField(auto_now_add=True)
    viewed_date = models.DateTimeField(blank=True, null=True)
    # mail_send = models.BooleanField(default=False)
    mail_starred = models.BooleanField(default=False)
    mail_spam = models.BooleanField(default=False)
    mail_deleted = models.BooleanField(default=False)
    mail_viewed = models.BooleanField(default=False)
    is_mail = models.BooleanField(default=False)
    receiver = models.ForeignKey(MemberInfo, on_delete=models.CASCADE, related_name="mail_receiver")
    mail = models.ForeignKey(Mail, on_delete=models.CASCADE)

    def __str__(self):
        return self.mail.subject
    # + '--' + self.mail.sender.username + '--' + self.receiver.username

    def get_file_upload_name(self):
        if self.mail.attachment:
            return os.path.split(self.mail.attachment.name)[1]
        else:
            return ""

    def delete(self, *args, **kwargs):
        mail_obj = self.mail
        super().delete()
        if mail_obj:
            if mail_obj.can_delete() and mail_obj.sender_delete_p:
                mail_obj.delete()

# @receiver(models.signals.post_delete, sender=MailReceiver)
# def delete_mail(sender, instance, *args, **kwargs):
#     """ Deletes mail on `post_delete` """
#     print(instance)
#     if instance.mail:
#         if instance.mail.can_delete() and instance.mail.sender_delete_p:
#             print("deleting mail")
#             instance.mail.delete()
#         else:
#             print("cant delete mail")
