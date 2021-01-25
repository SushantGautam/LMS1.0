from datetime import datetime, timedelta

from django.db import models
from django.utils.translation import gettext, ugettext_lazy as _

from WebApp.models import MemberInfo, ChapterInfo

EVENT_TYPE_CHOICES = (('PR', _('Program')),
                      ('ME', _('Meeting')),
                      ('HO', _('Holiday')),
                      ('EX', _('Examination')),
                      ('AS', _('Assignment')),
                      ('SR', _('Survey')),
                      ('CH', _('Chapter')))

REPEAT_TYPE_CHOICES = (('DA', _('Daily')),
                       ('WE', _('Weekly')),
                       ('MO', _('Monthly')),
                       ('WD', _('Weekdays')))

PART_TYPE_CHOICES = (('AL', _('All User')),
                     ('AT', _('All Teacher')),
                     ('AS', _('All Student')),
                     ('CH', _('Choose User')))


class CalendarEvent(models.Model):
    title = models.CharField(max_length=200, verbose_name=_('Title'))
    event_type = models.CharField(max_length=2, default='PR', choices=EVENT_TYPE_CHOICES, verbose_name=_('Event Type'))
    repeat_type = models.CharField(max_length=2, default='DA', choices=REPEAT_TYPE_CHOICES, verbose_name=_('Repeat Type'))
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
    chapters = models.ManyToManyField(ChapterInfo, verbose_name=_('Chapters'), blank=True)
    # chapters = models.CharField(max_length=1000, blank=True, null=True)

    def __str__(self):
        return self.title

    def get_participants(self):
        participant_list = self.participants.all()
        # print(type(participant_list))
        # print(participant_list)
        return participant_list

    def get_chapters(self):
        chapter_list = self.chapters.all()
        print("ChapterS", chapter_list)
        return chapter_list

    # def get_chapters(self):
    #     chapter_list = self.chapters
    #     if len(chapter_list):
    #         c_list = chapter_list.split(',')
    #         print(c_list)
    #         print([int(c) for c in c_list])
    #         return [int(c) for c in c_list]

    def get_end_date(self):
        if self.is_all_day:
            dt_string = str(self.date_end.date()) + " 23:59"
            # new_date = self.date_end + timedelta(hours=23, seconds=59)
            # return new_date.strftime("%Y-%m-%dT%H:%M:%SZ")
            return self.date_end.strftime("%Y-%m-%dT%H:%M:%SZ")
        else:
            return self.date_end.strftime("%Y-%m-%dT%H:%M:%SZ")

    class Meta:
        verbose_name = _("Calendar Event")
        verbose_name_plural = _("Calendar Events")
