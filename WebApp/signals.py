from datetime import timedelta

from django.contrib.contenttypes.models import ContentType
from django.db.models.signals import post_save, post_delete
from django.utils import timezone

from Notifications.models import Notification
from Notifications.signals import notify
from WebApp.models import CourseInfo, MemberInfo, ChapterInfo, InningInfo, InningGroup


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


def ChapterInfoCreate_handler(sender, instance, created, **kwargs):
    import inspect
    for frame_record in inspect.stack():
        if frame_record[3] == 'get_response':
            request = frame_record[0].f_locals['request']
            break
    else:
        request = None
    if created:
        verb = "created"
        description = '{} created chapter {} in course {}'.format(request.user, instance.Chapter_Name,
                                                                  instance.Course_Code.Course_Name)
    else:
        verb = "updated"
        description = '{} updated chapter {} in course {}'.format(request.user, instance.Chapter_Name,
                                                                  instance.Course_Code.Course_Name)

    notify.send(
        sender=request.user,
        verb=verb,
        recipient=MemberInfo.objects.filter(Center_Code=instance.Course_Code.Center_Code, Use_Flag=True,
                                            Is_CenterAdmin=True),
        description=description,
        action_object=instance,
    )

    '''
        Check if the chapter belonging to course is associated with any innings.
        If yes, add Session to notification table (target_audience).
        When the Notification start date is less than current time, send notification to all students in that session
        and delete the current object holding session information.
    '''

    if not created:
        # Update Notifications that have not been sent to receipents if instance is update
        NotificationAction(instance, instance.__class__, instance.id).update()

        if instance.Start_Date:
            if instance.Start_Date >= timezone.now():
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
                    description=description,
                    action_object=instance,
                )

    # --------------------------------------------------------------------------------

    if instance.Start_Date:
        if instance.Start_Date <= timezone.now():
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
                    description=description,
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
            description=description,
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

    notify.send(
        sender=request.user,
        verb=verb,
        recipient=MemberInfo.objects.filter(Center_Code=instance.Course_Code.Center_Code, Use_Flag=True,
                                            Is_CenterAdmin=True),
        description='{} deleted chapter {} from Course {}'.format(request.user, instance.Chapter_Name,
                                                                  instance.Course_Code.Course_Name),
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


class NotificationAction:
    def __init__(self, instance, action_object_content_type, action_object_object_id):
        self.instance, self.action_object_content_type, action_object_object_id = instance, action_object_content_type, action_object_object_id

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
                    self.instance.Start_Date - timedelta(hours=1, minutes=0)) if self.instance.Start_Date else None,
            end_notification_date=(
                    self.instance.End_Date - timedelta(hours=1, minutes=0)) if self.instance.End_Date else None,
        )
