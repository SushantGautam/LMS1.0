from django.db import models
from django.utils.translation import gettext, ugettext_lazy as _

from WebApp.models import MemberInfo

EVENT_TYPE_CHOICES = (('AP', _('Appointment')),
                      ('MT', _('Meeting')))


class CalendarEvent(models.Model):
    title = models.CharField(max_length=200, verbose_name=_('Title'))
    event_type = models.CharField(max_length=2, default='AP', choices=EVENT_TYPE_CHOICES, verbose_name=_('Event Type'))
    date_created = models.DateTimeField(auto_now_add=True, verbose_name=_('Created Date'))
    date_updated = models.DateTimeField(auto_now=True, verbose_name=_('Updated Date'))
    date_start = models.DateTimeField(verbose_name=_('Start Date'))
    date_end = models.DateTimeField(verbose_name=_('End Date'))
    description = models.TextField(blank=True, null=True, verbose_name=_('Description'))

    # ## Relational Fields:
    register_agent = models.ForeignKey(MemberInfo, related_name='calendar_events', on_delete=models.CASCADE,
                                       verbose_name=_('Register Agent'))
    participants = models.ManyToManyField(MemberInfo, verbose_name=_('Participants'), blank=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _("Calendar Event")
        verbose_name_plural = _("Calendar Events")
