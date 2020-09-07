from datetime import datetime

from django.db import models
from django.utils.translation import gettext, ugettext_lazy as _

from WebApp.models import MemberInfo

EVENT_TYPE_CHOICES = (('PR', _('Program')),
                      ('ME', _('Meeting')),
                      ('HO', _('Holiday')))
PART_TYPE_CHOICES = (('AL', _('All User')),
                     ('AT', _('All Teacher')),
                     ('AS', _('All Student')),
                     ('CH', _('Choose User')))


class CalendarEvent(models.Model):
    title = models.CharField(max_length=200, verbose_name=_('Title'))
    event_type = models.CharField(max_length=2, default='PR', choices=EVENT_TYPE_CHOICES, verbose_name=_('Event Type'))
    participation_type = models.CharField(max_length=2, default='AL', choices=PART_TYPE_CHOICES,
                                          verbose_name=_('Participation Type'))

    date_created = models.DateTimeField(auto_now_add=True, verbose_name=_('Created Date'))
    date_updated = models.DateTimeField(auto_now=True, verbose_name=_('Updated Date'))
    date_start = models.DateTimeField(verbose_name=_('Start Date'))
    date_end = models.DateTimeField(verbose_name=_('End Date'))
    description = models.TextField(blank=True, null=True, verbose_name=_('Description'))
    is_all_day = models.BooleanField(default=True, verbose_name=_('All Day Event'))

    # ## Relational Fields:
    register_agent = models.ForeignKey(MemberInfo, related_name='calendar_events', on_delete=models.CASCADE,
                                       verbose_name=_('Register Agent'))
    participants = models.ManyToManyField(MemberInfo, verbose_name=_('Participants'), blank=True)

    def __str__(self):
        return self.title

    def get_participants(self):
        participant_list = self.participants.all()
        # print(type(participant_list))
        # print(participant_list)
        return participant_list

    def get_end_date(self):
        if self.is_all_day:
            dt_string = str(self.date_end.date()) + " 23:59"
            return datetime.strptime(dt_string, "%Y-%m-%d %H:%M")
        else:
            return self.date_end

    class Meta:
        verbose_name = _("Calendar Event")
        verbose_name_plural = _("Calendar Events")
