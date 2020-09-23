from datetime import timedelta, datetime

from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError
from django.db.models.signals import post_save, post_delete, pre_save
from django.utils import timezone

from Notifications.models import Notification
from Notifications.signals import notify
from WebApp.models import CourseInfo, MemberInfo, InningInfo, InningGroup, AssignAnswerInfo, SessionMapInfo


# Multiple Submission of Assignment Prevention
def MultipleAssignmentSubmission(sender, instance, **kwargs):
    import inspect
    for frame_record in inspect.stack():
        if frame_record[3] == 'get_response':
            request = frame_record[0].f_locals['request']
            break
    else:
        request = None

    if instance.pk is None:
        if AssignAnswerInfo.objects.filter(Student_Code=request.user, Question_Code=instance.Question_Code).exists():
            raise ValidationError('Answer already exists.')


pre_save.connect(MultipleAssignmentSubmission, sender=AssignAnswerInfo)


class NotificationAction:
    def __init__(self, instance, action_object_content_type, action_object_object_id, start_date_field_name=None,
                 end_date_field_name=None):
        self.instance, self.action_object_content_type, action_object_object_id = instance, action_object_content_type, action_object_object_id
        if start_date_field_name and end_date_field_name:
            self.start_date_field_name, self.end_date_field_name = start_date_field_name, end_date_field_name
        else:
            self.start_date_field_name, self.end_date_field_name = self.instance.Start_Date, self.instance.End_Date

    def delete(self):
        # Filter Notifications of this that are not sent and delete.
        notifications_to_delete = Notification.objects.filter(is_sent=False, start_notification_date__gt=timezone.now(),
                                                              action_object_content_type=ContentType.objects.get_for_model(
                                                                  self.instance.__class__),
                                                              action_object_object_id=self.instance.id)
        notifications_to_delete.delete()

    def update(self):
        # Filter Notifications of this that are not sent and delete.
        notifications_to_update = Notification.objects.filter(is_sent=False, start_notification_date__gt=timezone.now(),
                                                              action_object_content_type=ContentType.objects.get_for_model(
                                                                  self.instance.__class__),
                                                              action_object_object_id=self.instance.id)

        notifications_to_update.update(
            start_notification_date=(
                    self.start_date_field_name - timedelta(hours=1, minutes=0)) if self.start_date_field_name else None,
            end_notification_date=(
                    self.end_date_field_name - timedelta(hours=1, minutes=0)) if self.end_date_field_name else None,
        )


def CourseInfoCreate_handler(sender, instance, created, **kwargs):
    import inspect
    for frame_record in inspect.stack():
        if frame_record[3] == 'get_response':
            request = frame_record[0].f_locals['request']
            break
    else:
        request = None
    if created:
        verb = "created"
    else:
        verb = "updated"
    notify.send(
        sender=request.user,
        # verb=kwargs.pop('verb'),
        verb=verb,
        recipient=MemberInfo.objects.filter(Center_Code=instance.Center_Code, Use_Flag=True, Is_CenterAdmin=True),
        description='{} created course {}'.format(request.user, instance.Course_Name),
        action_object=instance,
    )


post_save.connect(CourseInfoCreate_handler, sender=CourseInfo)


# To pass parameter to handler function.
# post_save.connect(
#     receiver=partial(CourseInfoCreate_handler,
#                      verb="created"),
#     sender=CourseInfo,
#     weak=False,
# )

def CourseInfoDelete_handler(sender, instance, **kwargs):
    import inspect
    for frame_record in inspect.stack():
        if frame_record[3] == 'get_response':
            request = frame_record[0].f_locals['request']
            break
    else:
        request = None
    notify.send(
        sender=request.user,
        verb='deleted',
        description='{} deleted course {}'.format(request.user, instance.Course_Name),
        recipient=MemberInfo.objects.filter(Center_Code=instance.Center_Code, Use_Flag=True, Is_CenterAdmin=True),
        action_object=instance,
    )


post_delete.connect(CourseInfoDelete_handler, sender=CourseInfo)

# post_delete.connect(
#     receiver=partial(CourseInfoDelete_handler,
#                      verb="deleted",
#                      ),
#     sender=CourseInfo,
#     weak=False,
# )

""""
def ChapterInfoCreate_handler(sender, instance, created, **kwargs):
    import inspect
    for frame_record in inspect.stack():
        if frame_record[3] == 'get_response':
            request = frame_record[0].f_locals['request']
            break
    else:
        request = None

    if instance.Start_Date:
        student_description = '{} will start from {} today ({})'.format(instance.Chapter_Name,
                                                                        datetime.strftime(instance.Start_Date,
                                                                                          "%H:%M"),
                                                                        datetime.strftime(instance.Start_Date,
                                                                                          "%d-%m-%Y"))
    else:
        student_description = '{} will start from {} today ({})'.format(instance.Chapter_Name,
                                                                        datetime.strftime(datetime.utcnow(),
                                                                                          "%H:%M"),
                                                                        datetime.strftime(datetime.utcnow(),
                                                                                          "%d-%m-%Y"))
    if created:
        verb = "created"
        description = '{} created chapter {} in course {}'.format(request.user, instance.Chapter_Name,
                                                                  instance.Course_Code.Course_Name)
    else:
        verb = "updated"
        description = '{} updated chapter {} in course {}'.format(request.user, instance.Chapter_Name,
                                                                  instance.Course_Code.Course_Name)

    # notify.send(
    #     sender=request.user,
    #     verb=verb,
    #     recipient=MemberInfo.objects.filter(Center_Code=instance.Course_Code.Center_Code, Use_Flag=True,
    #                                         Is_CenterAdmin=True),
    #     description=description,
    #     action_object=instance,
    # )

    '''
        Check if the chapter belonging to course is associated with any innings.
        If yes, add Session to notification table (target_audience).
        When the Notification start date is less than current time, send notification to all students in that session
        and delete the current object holding session information.
    '''

    if not created:
        # Update Notifications that have not been sent to receipents if instance is update
        NotificationAction(instance, instance.__class__, instance.id).update()

        '''
            When Editing the chapter, if the start date is changed, and start date is set to future date, then create a 
            future notification with target audience.
        '''
        if instance.Start_Date:
            if instance.Start_Date >= timezone.now():
                if not Notification.objects.filter(is_sent=False, start_notification_date__gt=timezone.now(),
                                                   action_object_content_type=ContentType.objects.get_for_model(
                                                       instance.__class__),
                                                   action_object_object_id=instance.id).exists():
                    notify.send(
                        start_notification_date=(
                                instance.Start_Date - timedelta(hours=1,
                                                                minutes=0)) if instance.Start_Date else timezone.now(),
                        end_notification_date=(
                                instance.End_Date - timedelta(hours=1, minutes=0)) if instance.End_Date else None,
                        sender=request.user,
                        target_audience=InningInfo.objects.filter(
                            Course_Group__in=InningGroup.objects.filter(Course_Code__pk=instance.Course_Code.pk)),
                        verb=verb,
                        description=student_description,
                        action_object=instance,
                    )

    # --------------------------------------------------------------------------------
    else:
        if instance.Start_Date and instance.Start_Date >= timezone.now():
            if InningInfo.objects.filter(
                    Course_Group__in=InningGroup.objects.filter(Course_Code__pk=instance.Course_Code.pk)).exists():
                notify.send(
                    start_notification_date=(
                            instance.Start_Date - timedelta(hours=1,
                                                            minutes=0)) if instance.Start_Date else timezone.now(),
                    end_notification_date=(
                            instance.End_Date - timedelta(hours=1, minutes=0)) if instance.End_Date else None,
                    sender=request.user,
                    target_audience=InningInfo.objects.filter(
                        Course_Group__in=InningGroup.objects.filter(Course_Code__pk=instance.Course_Code.pk)),
                    verb=verb,
                    description=student_description,
                    action_object=instance,
                )
        else:
            notify.send(
                start_notification_date=timezone.now(),
                end_notification_date=None,
                sender=request.user,
                target_audience=InningInfo.objects.filter(
                    Course_Group__in=InningGroup.objects.filter(Course_Code__pk=instance.Course_Code.pk)),
                verb=verb,
                description=student_description,
                action_object=instance,
            )


post_save.connect(ChapterInfoCreate_handler, sender=ChapterInfo)


def ChapterInfoDelete_handler(sender, instance, **kwargs):
    import inspect
    for frame_record in inspect.stack():
        if frame_record[3] == 'get_response':
            request = frame_record[0].f_locals['request']
            break
    else:
        request = None

    verb = 'deleted'

    # For admin

    # notify.send(
    #     sender=request.user,
    #     verb=verb,
    #     recipient=MemberInfo.objects.filter(Center_Code=instance.Course_Code.Center_Code, Use_Flag=True,
    #                                         Is_CenterAdmin=True),
    #     description='{} deleted chapter {} from Course {}'.format(request.user, instance.Chapter_Name,
    #                                                               instance.Course_Code.Course_Name),
    #     action_object=instance,
    # )
    # ----------------------------------------------------------------------------------------------------
    '''
        For Students, 

        Check if the chapter belonging to course is associated with any innings.
        If yes, add Session to notification table (target_audience).
        When the Notification start date is less than current time, send notification to all students in that session
        and delete the current object holding session information.
    '''

    # Delete Notifications that have not been sent to receipents if instance is deleted
    NotificationAction(instance, instance.__class__, instance.id).delete()

    # --------------------------------------------------------------------------------

    # If instance has start date and start date has been reached, then send delete notifications, except pass.
    if instance.Start_Date:
        if instance.Start_Date <= timezone.now():
            if InningInfo.objects.filter(
                    Course_Group__in=InningGroup.objects.filter(Course_Code__pk=instance.Course_Code.pk)).exists():
                notify.send(
                    sender=request.user,
                    target_audience=InningInfo.objects.filter(
                        Course_Group__in=InningGroup.objects.filter(Course_Code__pk=instance.Course_Code.pk)),
                    verb=verb,
                    description='{} deleted chapter {} in course {}'.format(request.user, instance.Chapter_Name,
                                                                            instance.Course_Code.Course_Name),
                    action_object=instance,
                )
    else:
        if InningInfo.objects.filter(
                Course_Group__in=InningGroup.objects.filter(Course_Code__pk=instance.Course_Code.pk)).exists():
            notify.send(
                sender=request.user,
                target_audience=InningInfo.objects.filter(
                    Course_Group__in=InningGroup.objects.filter(Course_Code__pk=instance.Course_Code.pk)),
                verb=verb,
                description='{} deleted chapter {} in course {}'.format(request.user, instance.Chapter_Name,
                                                                        instance.Course_Code.Course_Name),
                action_object=instance,
            )


post_delete.connect(ChapterInfoDelete_handler, sender=ChapterInfo)
"""

"""
def AssignmentInfoCreate_handler(sender, instance, created, **kwargs):
    import inspect
    for frame_record in inspect.stack():
        if frame_record[3] == 'get_response':
            request = frame_record[0].f_locals['request']
            break
    else:
        request = None

    if instance.Assignment_Start:
        student_description = 'Assignment {} will start from {} today ({})'.format(instance.Assignment_Topic,
                                                                                   datetime.strftime(
                                                                                       instance.Assignment_Start,
                                                                                       "%H:%M"),
                                                                                   datetime.strftime(
                                                                                       instance.Assignment_Start,
                                                                                       "%d-%m-%Y"))
    else:
        student_description = 'Assignment {} will start from {} today ({})'.format(instance.Assignment_Topic,
                                                                                   datetime.strftime(datetime.utcnow(),
                                                                                                     "%H:%M"),
                                                                                   datetime.strftime(datetime.utcnow(),
                                                                                                     "%d-%m-%Y"))
    if created:
        verb = "created"
        description = '{} created Assignment {} in chapter {}'.format(request.user, instance.Assignment_Topic,
                                                                      instance.Course_Code.Course_Name)
    else:
        verb = "updated"
        description = '{} updated Assignment {} in chapter {}'.format(request.user, instance.Assignment_Topic,
                                                                      instance.Chapter_Code.Chapter_Name)

    # notify.send(
    #     sender=request.user,
    #     verb=verb,
    #     recipient=MemberInfo.objects.filter(Center_Code=instance.Course_Code.Center_Code, Use_Flag=True,
    #                                         Is_CenterAdmin=True),
    #     description=description,
    #     action_object=instance,
    # )

    '''
        Check if the assignment belonging to course is associated with any innings.
        If yes, add Session to notification table (target_audience).
        When the Notification start date is less than current time, send notification to all students in that session
        and delete the current object holding session information.
    '''

    if not created:
        # Update Notifications that have not been sent to receipents if instance is update
        NotificationAction(instance, instance.__class__, instance.id, instance.Assignment_Start,
                           instance.Assignment_Deadline).update()

        '''
            When Editing the chapter, if the start date is changed, and start date is set to future date, then create a 
            future notification with target audience.
        '''
        if instance.Assignment_Start and instance.Assignment_Start >= timezone.now():
            if not Notification.objects.filter(is_sent=False, start_notification_date__gt=timezone.now(),
                                               action_object_content_type=ContentType.objects.get_for_model(
                                                   instance.__class__),
                                               action_object_object_id=instance.id).exists():
                notify.send(
                    start_notification_date=(
                            instance.Assignment_Start - timedelta(hours=1,
                                                                  minutes=0)) if instance.Assignment_Start else timezone.now(),
                    end_notification_date=(
                            instance.Assignment_Deadline - timedelta(hours=1,
                                                                     minutes=0)) if instance.Assignment_Deadline else None,
                    sender=request.user,
                    target_audience=InningInfo.objects.filter(
                        Course_Group__in=InningGroup.objects.filter(Course_Code__pk=instance.Course_Code.pk)),
                    verb=verb,
                    description=student_description,
                    action_object=instance,
                )

    # --------------------------------------------------------------------------------
    else:
        if instance.Assignment_Start and instance.Assignment_Start >= timezone.now():
            if InningInfo.objects.filter(
                    Course_Group__in=InningGroup.objects.filter(Course_Code__pk=instance.Course_Code.pk)).exists():
                notify.send(
                    start_notification_date=(
                            instance.Assignment_Start - timedelta(hours=1,
                                                                  minutes=0)) if instance.Assignment_Start else timezone.now(),
                    end_notification_date=(
                            instance.Assignment_Deadline - timedelta(hours=1,
                                                                     minutes=0)) if instance.Assignment_Deadline else None,
                    sender=request.user,
                    target_audience=InningInfo.objects.filter(
                        Course_Group__in=InningGroup.objects.filter(Course_Code__pk=instance.Course_Code.pk)),
                    verb=verb,
                    description=student_description,
                    action_object=instance,
                )
        else:
            notify.send(
                start_notification_date=timezone.now(),
                end_notification_date=None,
                sender=request.user,
                target_audience=InningInfo.objects.filter(
                    Course_Group__in=InningGroup.objects.filter(Course_Code__pk=instance.Course_Code.pk)),
                verb=verb,
                description=student_description,
                action_object=instance,
            )


post_save.connect(AssignmentInfoCreate_handler, sender=AssignmentInfo)


def AssignmentInfoDelete_handler(sender, instance, **kwargs):
    import inspect
    for frame_record in inspect.stack():
        if frame_record[3] == 'get_response':
            request = frame_record[0].f_locals['request']
            break
    else:
        request = None

    verb = 'deleted'

    notify.send(
        sender=request.user,
        verb=verb,
        recipient=MemberInfo.objects.filter(Center_Code=instance.Course_Code.Center_Code, Use_Flag=True,
                                            Is_CenterAdmin=True),
        description='{} deleted Assignment {} in Chapter {}'.format(request.user, instance.Assignment_Topic,
                                                                    instance.Chapter_Code.Chapter_Name),
        action_object=instance,
    )

    '''
        For Students,

        Check if the chapter belonging to course is associated with any innings.
        If yes, add Session to notification table (target_audience).
        When the Notification start date is less than current time, send notification to all students in that session
        and delete the current object holding session information.
    '''

    # Delete Notifications that have not been sent to receipents if instance is deleted
    NotificationAction(instance, instance.__class__, instance.id, instance.Assignment_Start,
                       instance.Assignment_Deadline).delete()

    # --------------------------------------------------------------------------------

    # If instance has start date and start date has been reached, then send delete notifications, except pass.
    if instance.Assignment_Start:
        if instance.Assignment_Start <= timezone.now():
            if InningInfo.objects.filter(
                    Course_Group__in=InningGroup.objects.filter(Course_Code__pk=instance.Course_Code.pk)).exists():
                notify.send(
                    sender=request.user,
                    target_audience=InningInfo.objects.filter(
                        Course_Group__in=InningGroup.objects.filter(Course_Code__pk=instance.Course_Code.pk)),
                    verb=verb,
                    description='{} deleted Assignment {} in Chapter {}'.format(request.user, instance.Assignment_Topic,
                                                                                instance.Chapter_Code.Chapter_Name),
                    action_object=instance,
                )
    else:
        if InningInfo.objects.filter(
                Course_Group__in=InningGroup.objects.filter(Course_Code__pk=instance.Course_Code.pk)).exists():
            notify.send(
                sender=request.user,
                target_audience=InningInfo.objects.filter(
                    Course_Group__in=InningGroup.objects.filter(Course_Code__pk=instance.Course_Code.pk)),
                verb=verb,
                description='{} deleted Assignment {} in Chapter {}'.format(request.user, instance.Assignment_Topic,
                                                                            instance.Chapter_Code.Chapter_Name),
                action_object=instance,
            )


post_delete.connect(AssignmentInfoDelete_handler, sender=AssignmentInfo)
"""


def InningMapCreate_handler(sender, instance, created, **kwargs):
    import inspect
    import dateutil
    for frame_record in inspect.stack():
        if frame_record[3] == 'get_response':
            request = frame_record[0].f_locals['request']
            break
    else:
        request = None

    start_date = instance.Start_Date
    end_date = instance.End_Date
    if isinstance(start_date, str) and start_date != '':
        start_date = dateutil.parser.parse(start_date)
    if isinstance(end_date, str) and start_date != '':
        end_date = dateutil.parser.parse(end_date)

    if start_date:
        student_description = '{} will start from {} today ({})'.format(instance.target,
                                                                        datetime.strftime(start_date,
                                                                                          "%H:%M"),
                                                                        datetime.strftime(start_date,
                                                                                          "%d-%m-%Y"))
    else:
        student_description = '{} will start from {} today ({})'.format(instance.target,
                                                                        datetime.strftime(datetime.utcnow(),
                                                                                          "%H:%M"),
                                                                        datetime.strftime(datetime.utcnow(),
                                                                                          "%d-%m-%Y"))
    if created:
        verb = "created"
        description = '{} created chapter {} in course {}'.format(request.user, instance.target,
                                                                  instance.target.Course_Code.Course_Name)
    else:
        verb = "updated"
        description = '{} updated chapter {} in course {}'.format(request.user, instance.target,
                                                                  instance.target.Course_Code.Course_Name)

    '''
        Check if the chapter/assignment belonging to course is associated with any innings.
        If yes, add Session to notification table (target_audience).
        When the Notification start date is less than current time, send notification to all students in that session
        and delete the current object holding session information.
    '''

    if not created:
        # Update Notifications that have not been sent to receipents if instance is update
        NotificationAction(instance.target, instance.target.__class__, instance.target.id, start_date,
                           end_date).update()

        '''
            When Editing the chapter, if the start date is changed, and start date is set to future date, then create a 
            future notification with target audience.
        '''
        if start_date:
            if start_date >= timezone.now():
                if not Notification.objects.filter(is_sent=False, start_notification_date__gt=timezone.now(),
                                                   action_object_content_type=ContentType.objects.get_for_model(
                                                       instance.target.__class__),
                                                   action_object_object_id=instance.target.id).exists():
                    notify.send(
                        start_notification_date=(
                                start_date - timedelta(hours=1,
                                                       minutes=0)) if start_date else timezone.now(),
                        end_notification_date=(
                                end_date - timedelta(hours=1, minutes=0)) if end_date else None,
                        sender=request.user,
                        target_audience=InningInfo.objects.filter(
                            Course_Group__in=InningGroup.objects.filter(
                                Course_Code__pk=instance.target.Course_Code.pk)),
                        verb=verb,
                        description=student_description,
                        action_object=instance.target,
                    )

    # --------------------------------------------------------------------------------
    else:
        if start_date and start_date >= timezone.now():
            if InningInfo.objects.filter(
                    Course_Group__in=InningGroup.objects.filter(
                        Course_Code__pk=instance.target.Course_Code.pk)).exists():
                notify.send(
                    start_notification_date=(
                            start_date - timedelta(hours=1,
                                                   minutes=0)) if start_date else timezone.now(),
                    end_notification_date=(
                            end_date - timedelta(hours=1, minutes=0)) if end_date else None,
                    sender=request.user,
                    target_audience=InningInfo.objects.filter(
                        Course_Group__in=InningGroup.objects.filter(Course_Code__pk=instance.target.Course_Code.pk)),
                    verb=verb,
                    description=student_description,
                    action_object=instance.target,
                )
        else:
            notify.send(
                start_notification_date=timezone.now(),
                end_notification_date=None,
                sender=request.user,
                target_audience=InningInfo.objects.filter(
                    Course_Group__in=InningGroup.objects.filter(Course_Code__pk=instance.target.Course_Code.pk)),
                verb=verb,
                description=student_description,
                action_object=instance.target,
            )


post_save.connect(InningMapCreate_handler, sender=SessionMapInfo)

