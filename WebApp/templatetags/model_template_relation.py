# This file contains template tags for template-model relation.

from django import template
from django.db.models import Sum
from django.urls import reverse
from django.utils import timezone

from WebApp.models import MemberInfo, AssignAnswerInfo, GroupMapping, InningInfo, InningGroup, CourseInfo, ChapterInfo, \
    AssignmentInfo

register = template.Library()


# For finding the submission status of surveys
@register.simple_tag
def getSurveyStatus(obj, user):
    can_submit, datetimeexpired, options, questions = obj.can_submit(user)
    return can_submit, datetimeexpired, options, questions


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
def getUserFullName(userdata):
    if MemberInfo.objects.filter(username=userdata).exists():
        return MemberInfo.objects.get(username=userdata).get_full_name()
    return '--'


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
def isCourseActive(userObj, courseObj):
    return courseObj in userObj.get_student_courses(activeCourse=True)['courses']

@register.simple_tag
def isChapterActive(userObj, chapterObj):
    return chapterObj.isStudentChapterActive(user=userObj)

@register.simple_tag
def isContentVisible(userObj, chapterObj):
    return chapterObj.isContentVisible(user=userObj)

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
            Session_Code=sessions) if sessions else object.chapter_sessionmaps.all

@register.simple_tag
def getQuizQuestionIndex(sitting, questionID):
    if str(questionID) in sitting.question_order.split(','):
        print(sitting.question_order.split(',').index(str(questionID)) + 1)
        return sitting.question_order.split(',').index(str(questionID)) + 1

import json
@register.simple_tag
def quizQuestion_check_if_answered(sitting, questionID):
    answers = dict(json.loads(sitting.user_answers))
    for qno, ans in answers.items():
        if qno == str(questionID):
            if isinstance(ans, str):
                if ans == '':
                    return False
            elif isinstance(ans, list):
                if len(ans) < 1:
                    return False
            return True


@register.simple_tag
def getStudentNotificationURL(object, user):
    from WebApp.student_module.views import student_active_chapters
    datetime_now = timezone.now()

    if object.__class__ in [ChapterInfo, AssignmentInfo]:
        student_groups = GroupMapping.objects.filter(Students=user)
        course_groups = InningGroup.objects.filter(Course_Code__pk=object.Course_Code.pk)
        assigned_session = InningInfo.objects.filter(Use_Flag=True,
                                                     Start_Date__lte=datetime_now,
                                                     End_Date__gte=datetime_now,
                                                     Groups__in=student_groups,
                                                     Course_Group__in=course_groups)

    if object.__class__ == ChapterInfo:
        active_chapters = student_active_chapters(CourseInfo.objects.filter(pk=object.Course_Code.pk),
                                                  assigned_session)

        if object in active_chapters:
            return reverse('student_chapterinfo_detail', args=(object.Course_Code.id, object.id))
        else:
            return reverse('student_courseinfo_detail', args=(object.Course_Code.id,))

    elif object.__class__ == AssignmentInfo:
        active_chapters = student_active_chapters(CourseInfo.objects.filter(pk=object.Course_Code.pk),
                                                  assigned_session)

        if object.Chapter_Code in active_chapters:
            return reverse('student_chapterinfo_detail', args=(object.Course_Code.id, object.Chapter_Code.id))
        else:
            return reverse('student_courseinfo_detail', args=(object.Course_Code.id,))

    else:
        return ''
