# This file contains template tags for template-model relation.

from django import template
from django.db.models import Sum
from django.utils import timezone

from WebApp.models import MemberInfo, AssignAnswerInfo

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


@register.simple_tag
def getUser(userdata):
    if MemberInfo.objects.filter(username=userdata).exists():
        return MemberInfo.objects.get(username=userdata)
    return userdata


@register.simple_tag
def getAssignmentsScore(assignmentObj, userObj):
    questions, answers = assignmentObj.get_QuestionAndAnswer(userObj)
    total_score = questions.aggregate(Question_Score__sum=Sum('Question_Score'))['Question_Score__sum']
    total_score_obtained = answers.aggregate(Assignment_Score__sum=Sum('Assignment_Score'))['Assignment_Score__sum']
    return {
        'questions': questions,
        'answers': answers,
        'total_score': total_score,
        'total_score_obtained': total_score_obtained if total_score_obtained else 0,
    }


@register.simple_tag
def getAssignmentAnswer(assignmentObj, userObj, questionObj):
    answer = AssignAnswerInfo.objects.filter(Question_Code=questionObj,
                                             Student_Code=userObj)
    if answer.exists():
        return answer.get(Question_Code=questionObj,
                          Student_Code=userObj)
    else:
        return None


@register.filter
def subtract(value, arg):
    return value - arg


@register.simple_tag
def isAssignmentActive(assignmentObj):
    inningmaps = assignmentObj.assignment_sessionmaps.all()
    isanswerable = False
    now = timezone.now()
    for inningmap in inningmaps:
        if inningmap.Start_Date <= now and inningmap.End_Date >= now:
            isanswerable = True
            break
    return isanswerable


@register.simple_tag
def getSessionMap(object, model_name, sessions=None):
    if model_name == 'assignmentinfo':
        return object.assignment_sessionmaps.filter(
            Session_Code=sessions) if sessions else object.assignment_sessionmaps.all
    elif model_name == 'chapterinfo':
        return object.chapter_sessionmaps.filter(
            Session_Code__in=sessions) if sessions else object.chapter_sessionmaps.all
