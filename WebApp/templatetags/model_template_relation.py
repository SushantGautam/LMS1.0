# This file contains template tags for template-model relation.

from django import template

register = template.Library()


# For finding the submission status of surveys
@register.simple_tag
def getSurveyStatus(obj, user):
    can_submit, datetimeexpired, options, questions = obj.can_submit(user)
    return can_submit, datetimeexpired, options, questions

# @register.simple_tag
# def canTakeQuiz(obj, user):
#     sitting = obj.can_take(user)
#     return sitting

@register.simple_tag
def getTeacherStatusoOfAssignment(obj, user):
    result = obj.getTeachersAssignmentStatus(user)
    completed = 0
    incomplete = 0
    for data in result:
        completed += len(data['completed_students'])
        incomplete += len(data['incompleted_students'])
    if incomplete > 0:
        assg_status = False
    else:
        assg_status = True
    return {
        'completed': completed,
        'incomplete': incomplete,
        'assg_status': assg_status,
        'total_students': completed + incomplete,
    }

@register.simple_tag
def getUserQuizStatus(obj, user):
    userSittings = obj.filter(user__id=user.id)
    if userSittings.exists():
        isExist = True
        for userSitting in userSittings:
            if userSitting.complete:
                isComplete = True
                break
            else:
                isComplete = False
    else:
        isExist = False
        isComplete = None
    return {
        'isExist': isExist,
        'isComplete': isComplete
    }
