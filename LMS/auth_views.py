from django.contrib import messages
from django.shortcuts import redirect, get_object_or_404

from WebApp.models import CourseInfo, MemberInfo, GroupMapping, InningInfo, InningGroup, ChapterInfo, AssignmentInfo
from quiz.models import Quiz, Sitting
from survey.models import SurveyInfo


class AdminAuthMxnCls:
    def get(self, request, *args, **kwargs):
        # Checks if AuthCheck passed test for admin by returning 1 else exits
        return super().get(request, *args, **kwargs) if AuthCheck(request, admn=1) == 1 else redirect('login')


class TeacherAuthMxnCls:
    def get(self, request, *args, **kwargs):
        # Checks if AuthCheck passed test for admin by returning 1 else exits
        return super().get(request, *args, **kwargs) if AuthCheck(request, tchr=1) == 1 else redirect('login')


class StudentAuthMxnCls:
    def get(self, request, *args, **kwargs):
        # Checks if AuthCheck passed test for admin by returning 1 else exits
        return super().get(request, *args, **kwargs) if AuthCheck(request, stdn=1) == 1 else redirect('login')


def AuthCheck(request, admn=0, tchr=0, stdn=0):
    initStat = 1
    try:
        if admn:
            if not request.user.Is_CenterAdmin:
                initStat *= 0
        if tchr:
            if not request.user.Is_Teacher:
                initStat *= 0

        if stdn:
            if not request.user.Is_Student:
                initStat *= 0
    except:
        return redirect('login')

    if initStat:
        return 1
    else:
        messages.error(request,
                       'The path you entered into the system was not suitable for your role and you were redirected.')
        return 2


# def returnMessageFunc(request):
#     return redirect('login')

def returnResultFunc(request):
    messages.error(request,
                   'The path you entered into the system was not suitable for your role and you were redirected.')
    return 2


class CourseAuthMxnCls:
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs) if CourseAuth(request,
                                                                   kwargs.get(
                                                                       'pk')) == 1 else redirect('login')


def CourseAuth(request, pk):
    return 1 if get_object_or_404(CourseInfo,
                                  pk=pk).Center_Code == request.user.Center_Code else returnResultFunc(request)


class TeacherCourseAuthMxnCls:
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs) if TeacherCourseAuth(request,
                                                                          kwargs.get(
                                                                              'pk')) == 1 else redirect('login')


def TeacherCourseAuth(request, pk):
    return 1 if request.user in get_object_or_404(CourseInfo,
                                                  pk=pk).get_teachers_of_this_course() else returnResultFunc(request)


class StudentCourseAuthMxnCls:
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs) if StudentCourseAuth(request,
                                                                          kwargs.get(
                                                                              'pk')) == 1 else redirect('login')


def StudentCourseAuth(request, pk):
    courselist = []
    for x in request.user.get_student_courses():
        for y in x:
            courselist.append(y)
    return 1 if get_object_or_404(CourseInfo, pk=pk).pk in courselist else returnResultFunc(
        request)


class ChapterAuthMxnCls:
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs) if ChapterAuth(request,
                                                                    kwargs.get(
                                                                        'pk')) == 1 else redirect('login')


class TeacherChapterAuthMxnCls:
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs) if TeacherCourseAuth(request,
                                                                          kwargs.get('course')) == 1 else redirect(
            'login')


class StudentChapterAuthMxnCls:
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs) if StudentCourseAuth(request,
                                                                          kwargs.get(
                                                                              'course')) == 1 else redirect('login')


def ChapterAuth(request, pk):
    return 1 if get_object_or_404(ChapterInfo,
                                  pk=pk).Course_Code.Center_Code == request.user.Center_Code else returnResultFunc(
        request)


class MemberAuthMxnCls:
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs) if MemberAuth(request,
                                                                   kwargs.get(
                                                                       'pk')) == 1 else redirect('login')


def MemberAuth(request, pk):
    return 1 if get_object_or_404(MemberInfo,
                                  pk=pk).Center_Code == request.user.Center_Code else returnResultFunc(request)


class GroupMappingAuthMxnCls:
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs) if GroupMappingAuth(request,
                                                                         kwargs.get(
                                                                             'pk')) == 1 else redirect('login')


def GroupMappingAuth(request, pk):
    return 1 if get_object_or_404(GroupMapping,
                                  pk=pk).Center_Code == request.user.Center_Code else returnResultFunc(request)


class InningInfoAuthMxnCls:
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs) if InningInfoAuth(request,
                                                                       kwargs.get(
                                                                           'pk')) == 1 else redirect('login')


def InningInfoAuth(request, pk):
    return 1 if get_object_or_404(InningInfo,
                                  pk=pk).Center_Code == request.user.Center_Code else returnResultFunc(request)


class InningGroupAuthMxnCls:
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs) if InningGroupAuth(request,
                                                                        kwargs.get(
                                                                            'pk')) == 1 else redirect('login')


def InningGroupAuth(request, pk):
    return 1 if get_object_or_404(InningGroup,
                                  pk=pk).Center_Code == request.user.Center_Code else returnResultFunc(request)


class SurveyInfoAuthMxnCls:
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs) if SurveyInfoAuth(request,
                                                                       kwargs.get(
                                                                           'pk')) == 1 else redirect('login')


def SurveyInfoAuth(request, pk):
    return 1 if SurveyInfo.objects.get(
        pk=pk).Center_Code == request.user.Center_Code else returnResultFunc(request)


# class ForumTopicAuthMxnCls:
#     def get(self, request, *args, **kwargs):
#         return super().get(request, *args, **kwargs) if ForumTopicAuth(request,
#                                                                    kwargs.get(
#                                                                        'pk')) == 1 else redirect('login')
#
# def ForumTopicAuth(request, pk):
#     return 1 if Topic.objects.get(
#         pk=pk).center_associated_with == request.user.Center_Code else returnResultFunc(request)

class AssignmentInfoAuthMxnCls:
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs) if AssignmentInfoAuth(request,
                                                                           kwargs.get(
                                                                               'pk')) == 1 else redirect('login')


def AssignmentInfoAuth(request, pk):
    return 1 if AssignmentInfo.objects.get(
        pk=pk).Course_Code.Center_Code == request.user.Center_Code else returnResultFunc(request)


class TeacherAssignmentAuthMxnCls:
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs) if TeacherCourseAuth(request,
                                                                          kwargs.get('course')) == 1 else redirect(
            'login')


class StudentAssignmentAuthMxnCls:
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs) if StudentCourseAuth(request,
                                                                          kwargs.get(
                                                                              'course')) == 1 else redirect('login')


class QuizInfoAuthMxnCls:
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs) if QuizInfoAuth(request,
                                                                     kwargs.get(
                                                                         'pk')) == 1 else redirect('login')


def QuizInfoAuth(request, pk):
    return 1 if get_object_or_404(Quiz,
                                  pk=pk).course_code.Center_Code == request.user.Center_Code else returnResultFunc(
        request)


class SittingInfoAuthMxnCls:
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs) if SittingInfoAuth(request,
                                                                        kwargs.get(
                                                                            'pk')) == 1 else redirect('login')


def SittingInfoAuth(request, pk):
    return 1 if Sitting.objects.get(
        pk=pk).quiz.course_code.Center_Code == request.user.Center_Code else returnResultFunc(request)
