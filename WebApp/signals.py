from datetime import timedelta

from django.db.models.signals import post_save, post_delete

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
    else:
        verb = "updated"

    notify.send(
        sender=request.user,
        verb=verb,
        recipient=MemberInfo.objects.filter(Center_Code=instance.Course_Code.Center_Code, Use_Flag=True,
                                            Is_CenterAdmin=True),
        description='{} created chapter {} in course {}'.format(request.user, instance.Chapter_Name,
                                                                instance.Course_Code.Course_Name),
        action_object=instance,
    )

    '''
        Check if the chapter belonging to course is associated with any innings.
        If yes, add Session to notification table (target_audience).
        When the Notification start date is less than current time, send notification to all students in that session
        and delete the current object holding session information.
    '''

    if InningInfo.objects.filter(
            Course_Group__in=InningGroup.objects.filter(Course_Code__pk=instance.Course_Code.pk)).exists():
        notify.send(
            start_notification_date=(
                    instance.Start_Date - timedelta(hours=1, minutes=0)) if instance.Start_Date else None,
            end_notification_date=(instance.End_Date - timedelta(hours=1, minutes=0)) if instance.End_Date else None,
            sender=request.user,
            target_audience=InningInfo.objects.filter(
                Course_Group__in=InningGroup.objects.filter(Course_Code__pk=instance.Course_Code.pk)),
            verb=verb,
            description='{} created chapter {} in course {}'.format(request.user, instance.Chapter_Name,
                                                                    instance.Course_Code.Course_Name),
            action_object=instance,
        )


post_save.connect(ChapterInfoCreate_handler, sender=ChapterInfo)
