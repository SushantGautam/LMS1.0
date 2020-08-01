from django.contrib.auth.models import Group
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
# Create your models here.
from django.db.models import QuerySet
from django.utils import timezone
from model_utils import Choices

from Notifications.signals import notify
from WebApp.models import MemberInfo, InningInfo


class NotificationQuerySet(models.query.QuerySet):
    ''' Notification QuerySet '''

    def unread(self, include_deleted=False):
        """Return only unread items in the current queryset"""
        return self.filter(unread=True)

    def read(self, include_deleted=False):
        """Return only read items in the current queryset"""
        return self.filter(unread=False)

    def mark_all_as_read(self, recipient=None):
        """Mark as read any unread messages in the current queryset.

        Optionally, filter these by recipient first.
        """
        # We want to filter out read ones, as later we will store
        # the time they were marked as read.
        qset = self.unread(True)
        if recipient:
            qset = qset.filter(recipient=recipient)

        return qset.update(unread=False)

    def mark_all_as_unread(self, recipient=None):
        """Mark as unread any read messages in the current queryset.

        Optionally, filter these by recipient first.
        """
        qset = self.read(True)

        if recipient:
            qset = qset.filter(recipient=recipient)

        return qset.update(unread=True)


class Notification(models.Model):
    start_notification_date = models.DateTimeField(default=timezone.now)
    end_notification_date = models.DateTimeField(blank=True, null=True)

    LEVELS = Choices('success', 'info', 'warning', 'error')
    level = models.CharField(choices=LEVELS, default=LEVELS.info, max_length=20)
    verb = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    unread = models.BooleanField(default=True, blank=False, db_index=True)

    creator = models.ForeignKey(MemberInfo, on_delete=models.CASCADE, blank=False, related_name='notification_creator')
    recipient = models.ForeignKey(MemberInfo, on_delete=models.CASCADE, blank=True, null=True,
                                  related_name='notifications')

    target_audience = models.ForeignKey(InningInfo, on_delete=models.CASCADE, blank=True, null=True,
                                        related_name='pending_notifications')
    is_sent = models.BooleanField(default=True)

    target_content_type = models.ForeignKey(
        ContentType,
        related_name='notify_target',
        blank=True,
        null=True,
        on_delete=models.CASCADE
    )
    target_object_id = models.CharField(max_length=255, blank=True, null=True)
    target = GenericForeignKey('target_content_type', 'target_object_id')

    action_object_content_type = models.ForeignKey(ContentType, blank=True, null=True,
                                                   related_name='notify_action_object', on_delete=models.CASCADE)
    action_object_object_id = models.CharField(max_length=255, blank=True, null=True)
    action_object = GenericForeignKey('action_object_content_type', 'action_object_object_id')

    timestamp = models.DateTimeField(default=timezone.now)
    objects = NotificationQuerySet.as_manager()

    class Meta:
        ordering = ('-timestamp',)
        # speed up notifications count query
        index_together = ('recipient', 'unread')

    def __str__(self):
        ctx = {
            'actor': self.creator,
            'verb': self.verb,
            'action_object': self.action_object,
            'action_object_content_type': self.action_object_content_type,
            'recipient': self.recipient,
            'timesince': self.timesince()
        }
        if self.action_object:
            return u'%(actor)s %(verb)s %(action_object_content_type)s %(action_object)s %(timesince)s ago' % ctx
        return u'%(actor)s %(verb)s %(timesince)s ago' % ctx

    def timesince(self, now=None):
        """
        Shortcut for the ``django.utils.timesince.timesince`` function of the
        current timestamp.
        """
        from django.utils.timesince import timesince as timesince_
        return timesince_(self.start_notification_date, now)

    def mark_as_read(self):
        if self.unread:
            self.unread = False
            self.save()

    def mark_as_unread(self):
        if not self.unread:
            self.unread = True
            self.save()


def notify_handler(verb, **kwargs):
    """
    Handler function to create Notification instance upon action signal call.
    """
    # Pull the options out of kwargs
    kwargs.pop('signal', None)
    recipient = kwargs.pop('recipient', None)
    target_audience = kwargs.pop('target_audience', None)
    creator = kwargs.pop('sender')
    optional_objs = [
        (kwargs.pop(opt, None), opt)
        for opt in ('target', 'action_object')
    ]

    description = kwargs.pop('description', None)

    start_notification_date = kwargs.pop('start_notification_date', timezone.now())
    if not start_notification_date or start_notification_date < timezone.now():
        start_notification_date = timezone.now()
    end_notification_date = kwargs.pop('end_notification_date', None)
    timestamp = kwargs.pop('timestamp', timezone.now())

    level = kwargs.pop('level', Notification.LEVELS.info)

    new_notifications = []

    # Check if User or Group
    if recipient:
        if isinstance(recipient, Group):
            recipients = recipient.user_set.all()
        elif isinstance(recipient, (QuerySet, list)):
            recipients = recipient
        else:
            recipients = [recipient]

        for recipient in recipients:
            newnotify = Notification.objects.create(
                start_notification_date=start_notification_date,
                end_notification_date=end_notification_date,
                level=level,
                verb=str(verb),
                description=description,

                creator=creator,
                recipient=recipient,

                timestamp=timestamp,
            )

            # Set optional objects
            for obj, opt in optional_objs:
                if obj is not None:
                    setattr(newnotify, '%s_object_id' % opt, obj.pk)
                    setattr(newnotify, '%s_content_type' % opt,
                            ContentType.objects.get_for_model(obj))

            newnotify.save()
            new_notifications.append(newnotify)

    if target_audience:
        if isinstance(target_audience, (QuerySet, list)):
            target_audiences = target_audience
        else:
            target_audiences = [target_audience]

        for target_audience in target_audiences:
            newnotify = Notification.objects.create(
                start_notification_date=start_notification_date,
                end_notification_date=end_notification_date,
                level=level,
                verb=str(verb),
                description=description,

                creator=creator,
                target_audience=target_audience if target_audience else None,
                is_sent=False,

                timestamp=timestamp,
            )

            # Set optional objects
            for obj, opt in optional_objs:
                if obj is not None:
                    setattr(newnotify, '%s_object_id' % opt, obj.pk)
                    setattr(newnotify, '%s_content_type' % opt,
                            ContentType.objects.get_for_model(obj))

            newnotify.save()
            new_notifications.append(newnotify)

    return new_notifications


# connect the signal
notify.connect(notify_handler, dispatch_uid='Notifications.models.Notification')
