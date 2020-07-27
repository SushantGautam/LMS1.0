from django.db.models.signals import post_save, post_delete

from Notifications.signals import notify
from WebApp.models import CourseInfo, MemberInfo


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
