from datetime import timedelta, datetime

from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError
from django.db.models.signals import post_save, post_delete, pre_save
from django.utils import timezone

from Notifications.models import Notification
from Notifications.signals import notify
from WebApp.models import CourseInfo, MemberInfo, InningInfo, InningGroup, AssignAnswerInfo, SessionMapInfo, \
    AssignmentQuestionInfo, ChapterInfo, AssignmentInfo
# Multiple Submission of Assignment Prevention
from comment.models import Comment


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


# post_delete.connect(CourseInfoDelete_handler, sender=CourseInfo)


# Delete Chapter/Assignment all Notifications if the chapter/assignment instances are deleted
def ModelInfoDelete_handler(sender, instance, **kwargs):
    notifications = Notification.objects.filter(
        action_object_content_type=ContentType.objects.get_for_model(instance.__class__),
        action_object_object_id=instance.id).delete()


post_delete.connect(ModelInfoDelete_handler, sender=ChapterInfo)

post_delete.connect(ModelInfoDelete_handler, sender=AssignmentInfo)


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
                        target_audience=instance.Session_Code,
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
                    target_audience=instance.Session_Code,
                    verb=verb,
                    description=student_description,
                    action_object=instance.target,
                )
        else:
            notify.send(
                start_notification_date=timezone.now(),
                end_notification_date=None,
                sender=request.user,
                target_audience=instance.Session_Code,
                verb=verb,
                description=student_description,
                action_object=instance.target,
            )

    if instance.target.__class__ == AssignmentInfo:
        AssignmentDeadlineNotificationCreate(
            sender, instance, created,
            start_date=start_date,
            end_date=end_date,
            request=request,
            description='Assignment {} will expire on {}'.format(instance.target,
                                                                 datetime.strftime(instance.target.Assignment_Deadline,
                                                                                   "%d-%m-%Y %H:%M")),
            verb='expire',

        )


post_save.connect(InningMapCreate_handler, sender=SessionMapInfo)


def AssignmentDeadlineNotificationCreate(sender, instance, created, **kwargs):
    start_date = kwargs.get('start_date')
    end_date = kwargs.get('end_date')
    request = kwargs.get('request')
    student_description = kwargs.get('description')
    verb = kwargs.get('verb')
    if not created:
        # Update Notifications that have not been sent to receipents if instance is update
        NotificationAction(instance.target, instance.target.__class__, instance.target.id, start_date,
                           end_date).update()

        '''
            When Editing the chapter, if the start date is changed, and start date is set to future date, then create a 
            future notification with target audience.
        '''
        if end_date:
            if end_date >= timezone.now():
                if not Notification.objects.filter(is_sent=False, start_notification_date__gt=timezone.now(),
                                                   action_object_content_type=ContentType.objects.get_for_model(
                                                       instance.target.__class__),
                                                   action_object_object_id=instance.target.id).exists():
                    notify.send(
                        start_notification_date=(
                                end_date - timedelta(hours=1,
                                                     minutes=0)) if start_date else timezone.now(),
                        end_notification_date=end_date if end_date else None,
                        sender=request.user,
                        target_audience=instance.Session_Code,
                        verb=verb,
                        description=student_description,
                        action_object=instance.target,
                    )

    # --------------------------------------------------------------------------------
    else:
        if end_date and end_date >= timezone.now():
            if InningInfo.objects.filter(
                    Course_Group__in=InningGroup.objects.filter(
                        Course_Code__pk=instance.target.Course_Code.pk)).exists():
                notify.send(
                    start_notification_date=(
                            end_date - timedelta(hours=1,
                                                 minutes=0)) if start_date else timezone.now(),
                    end_notification_date=end_date if end_date else None,
                    sender=request.user,
                    target_audience=instance.Session_Code,
                    verb=verb,
                    description=student_description,
                    action_object=instance.target,
                )


def AssignmentQuestionInfoCreate_handler(sender, instance, created, **kwargs):
    import inspect
    for frame_record in inspect.stack():
        if frame_record[3] == 'get_response':
            request = frame_record[0].f_locals['request']
            break
    else:
        request = None

    if created:
        verb = "created"
        student_description = 'Question has been added to assignment "{}".'.format(
            instance.Assignment_Code.Assignment_Topic)
    else:
        verb = "updated"
        student_description = 'Question has been updated in assignment "{}".'.format(
            instance.Assignment_Code.Assignment_Topic)

    '''
        New Notification will be created in both cases.
    '''

    for sessionmap in instance.Assignment_Code.assignment_sessionmaps.filter(Start_Date__lte=timezone.now(),
                                                                             End_Date__gte=timezone.now()):
        if sessionmap.Session_Code.is_active:
            notify.send(
                sender=request.user,
                target_audience=sessionmap.Session_Code,
                verb=verb,
                description=student_description,
                action_object=instance,
            )


post_save.connect(AssignmentQuestionInfoCreate_handler, sender=AssignmentQuestionInfo)


def AssignmentQuestionInfoDelete_handler(sender, instance, **kwargs):
    import inspect
    for frame_record in inspect.stack():
        if frame_record[3] == 'get_response':
            request = frame_record[0].f_locals['request']
            break
    else:
        request = None

    verb = 'deleted'

    '''
        Delete Notification will be created.
    '''

    for sessionmap in instance.Assignment_Code.assignment_sessionmaps.filter(Start_Date__lte=timezone.now(),
                                                                             End_Date__gte=timezone.now()):
        if sessionmap.Session_Code.is_active:
            notify.send(
                sender=request.user,
                target_audience=sessionmap.Session_Code,
                verb=verb,
                description='Question has been deleted from assignment "{}".'.format(
                    instance.Assignment_Code.Assignment_Topic),
                action_object=instance,
            )


# post_delete.connect(AssignmentQuestionInfoDelete_handler, sender=AssignmentQuestionInfo)

def CommentCreate_handler(sender, instance, created, **kwargs):
    import inspect
    for frame_record in inspect.stack():
        if frame_record[3] == 'get_response':
            request = frame_record[0].f_locals['request']
            break
    else:
        request = None

    if created:
        if instance.parent:
            verb = "replied to your comment in"
            description = "{} replied to your comment in {}".format(request.user, instance.content_object)
        else:
            verb = "commented on"
            description = "{} commented on {}".format(request.user, instance.content_object)
    else:
        if request.POST.get('content'):
            verb = "updated comment"
            description = "{} updated comment in {}".format(request.user, instance.content_object)
        else:
            return
    action_object = instance.content_object

    # For creating notification for teachers of the chapter excluding oneself.

    """
        If the comment is created, all the teachers in the course will be notified. 
        If the comment is a reply, then only the main commentor will be notified.
    """
    if not instance.parent:
        if action_object.__class__ == ChapterInfo:
            recipients = action_object.Course_Code.get_teachers_of_this_course().exclude(pk=request.user.pk)
            notify.send(
                sender=request.user,
                recipient=recipients,
                verb=verb,
                description=description,
                action_object=action_object,
            )
    else:
        if action_object.__class__ == ChapterInfo:
            if request.user.pk != instance.parent.user.pk:
                recipients = action_object.Course_Code.get_teachers_of_this_course().exclude(pk=request.user.pk)
                notify.send(
                    sender=request.user,
                    recipient=instance.parent.user,
                    verb=verb,
                    description='',
                    action_object=action_object,
                )


post_save.connect(CommentCreate_handler, sender=Comment)


def CommentDelete_handler(sender, instance, **kwargs):
    import inspect
    for frame_record in inspect.stack():
        if frame_record[3] == 'get_response':
            request = frame_record[0].f_locals['request']
            break
    else:
        request = None

    if instance.parent:
        verb = "deleted your reply to the comment in"
    else:
        verb = "deleted your comment in"

    action_object = instance.content_object

    if action_object.__class__ == ChapterInfo:
        if request.user != instance.user:
            recipients = instance.user
            notify.send(
                sender=request.user,
                recipient=recipients,
                verb=verb,
                description='{} deleted your reply to the comment in {}'.format(request.user, action_object),
                action_object=action_object,
            )


post_delete.connect(CommentDelete_handler, sender=Comment)


def commentActionsHandler(request, instance, verb, description=''):
    if request.user.pk != instance.user.pk:
        notify.send(
            sender=request.user,
            recipient=instance.user,
            verb=verb,
            description=description,
            action_object=instance.content_object,
        )
