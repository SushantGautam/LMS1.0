# from django.core.checks import messages
import json
import os
import re
import shutil
from datetime import datetime, timedelta
from io import BytesIO

import pandas as pd
from django.conf import settings
# from django.core.checks import messages
from django.contrib import messages
from django.contrib.auth import get_user_model, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import PasswordContextMixin
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from django.db.models import Count
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.urls import reverse_lazy
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.utils.translation import gettext as _
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters
from django.views.generic import ListView, CreateView, DetailView, UpdateView, TemplateView, DeleteView
from django.views.generic.edit import FormView
from django_addanother.views import CreatePopupMixin

from LMS.auth_views import TeacherAuthMxnCls, CourseAuthMxnCls, InningInfoAuthMxnCls, InningInfoAuth, ChapterAuthMxnCls, \
    AssignmentInfoAuthMxnCls, SurveyInfoAuthMxnCls, GroupMappingAuthMxnCls, MemberAuth, InningGroupAuthMxnCls, \
    QuizInfoAuthMxnCls, TeacherCourseAuthMxnCls, TeacherChapterAuthMxnCls, TeacherAssignmentAuthMxnCls, \
    TeacherCourseAuth
from WebApp.forms import CourseInfoForm, ChapterInfoForm, AssignmentInfoForm, AttendanceForm, AttendanceFormSetForm, \
    AttendanceFormSetFormT
from WebApp.forms import GroupMappingForm, InningGroupForm, \
    InningInfoForm
from WebApp.forms import UserUpdateForm
from WebApp.models import CourseInfo, ChapterInfo, InningInfo, AssignmentQuestionInfo, AssignmentInfo, InningGroup, \
    AssignAnswerInfo, MemberInfo, GroupMapping, InningManager, Attendance, Notice, NoticeView
from forum.forms import ThreadForm, ThreadEditForm
from forum.models import NodeGroup, Thread, Topic
from forum.models import Post, Notification
from forum.views import get_top_thread_keywords
from quiz.forms import SAQuestionForm, QuizForm, QuestionForm, AnsFormset, MCQuestionForm, TFQuestionForm, \
    QuizBasicInfoForm
from quiz.models import Question, Quiz, SA_Question, MCQuestion, TF_Question, Answer
from quiz.views import QuizMarkerMixin, SittingFilterTitleMixin
from survey.forms import SurveyInfoForm, QuestionInfoFormset, QuestionAnsInfoFormset
from survey.models import CategoryInfo, SurveyInfo, QuestionInfo, OptionInfo, SubmitSurvey
from survey.views import AjaxableResponseMixin
from .forms import TopicForm, ReplyForm
from .misc import get_query

datetime_now = datetime.now()
from django.http import HttpResponseRedirect, HttpResponseForbidden, HttpResponse
from formtools.wizard.views import SessionWizardView
from quiz.forms import QuizForm1, QuizForm2, QuizForm3

from quiz.models import Progress

from django.http import JsonResponse

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

User = get_user_model()

from Notifications.signals import notify

def start(request):
    """Start page with a documentation.
    """
    # return render(request,"start.html")

    if request.user.Is_Teacher:
        wordCloud = Thread.objects.filter(user__Center_Code=request.user.Center_Code)
        thread_keywords = get_top_thread_keywords(request, 10)
        sessions = []

        x = request.user.get_teacher_courses()
        mycourse = x['courses']
        sessions_list = x['session']
        x = [x for x in sessions_list]
        for y in x:
            for z in y:
                if z not in sessions:
                    sessions.append(z)
        activeassignments = []
        for course in mycourse:
            activeassignments += AssignmentInfo.objects.filter(Course_Code=course,
                                                               Assignment_Deadline__gte=datetime_now,
                                                               Chapter_Code__Use_Flag=True)
        if Notice.objects.filter(Start_Date__lte=datetime.now(), End_Date__gte=datetime.now(),
                                 status=True).exists():
            notice = Notice.objects.filter(Start_Date__lte=datetime.now(), End_Date__gte=datetime.now(), status=True)[0]
            if NoticeView.objects.filter(notice_code=notice, user_code=request.user).exists():
                notice_view_flag = NoticeView.objects.filter(notice_code=notice, user_code=request.user)[0].dont_show
                if notice_view_flag:
                    notice = None
        else:
            notice = None

        return render(request, "teacher_module/homepage.html",
                      {'MyCourses': mycourse, 'Session': sessions, 'activeAssignments': activeassignments,
                       'wordCloud': wordCloud, 'notice': notice, 'get_top_thread_keywords': thread_keywords})
    else:
        return redirect('login')


def teacher_editprofile(request):
    if not request.user.is_authenticated:
        return HttpResponse("you are not authenticated", {'error_message': 'Error Message Customize here'})

    post = get_object_or_404(MemberInfo, pk=request.user.id)
    if request.method == "POST":

        form = UserUpdateForm(request.POST, request.FILES, instance=post)

        if form.is_valid():
            post.date_last_update = datetime.now()
            post.save()
            return redirect('teacher_user_profile')
    else:

        form = UserUpdateForm(request.POST, request.FILES, instance=post)

    return render(request, 'teacher_module/editprofile.html', {'form': form})


def Dashboard(request):
    return render(request, 'teacher_module/homepage.html', )


class GroupMappingDetailViewTeacher(GroupMappingAuthMxnCls, DetailView):
    model = GroupMapping
    template_name = 'teacher_module/groupmapping_detail.html'


from quiz.views import QuizUserProgressView, Sitting


def Student_DetailInfo(request, id):
    if MemberAuth(request, id) != 1:
        return redirect('login')
    memberinfo = MemberInfo.objects.get(pk=id)
    groupmapping = GroupMapping.objects.filter(Students__in=[id])[0]
    sittings = Sitting.objects.filter(user=memberinfo)
    return render(request, 'teacher_module/student_detail.html',
                  {'memberinfo': memberinfo, 'sittings': sittings, 'groupmapping': groupmapping})


class QuestionInfoDeleteView(DeleteView):
    model = AssignmentQuestionInfo

    # Assignment_Code = get_object_or_404(AssignmentInfo, pk=self.kwargs.get('assignment'))

    def post(self, request, *args, **kwargs):

        try:
            # return self.delete(request, *args, **kwargs)
            Obj = AssignmentQuestionInfo.objects.get(pk=self.request.POST['question_id'])
            Obj.delete()
            return redirect('teacher_assignmentinfo_detail', course=request.POST['course_id'],
                            chapter=request.POST['chapter_id'], pk=request.POST['assignment_id'])

        except:
            messages.error(request,
                           "Fail")
            return redirect('teacher_assignmentinfo_detail', course=request.POST['course_id'],
                            chapter=request.POST['chapter_id'], pk=request.POST['assignment_id'])
            # return redirect('student_home')
    # success_url = reverse_lazy('assignmentinfo_detail', course=self.request.POST['course_id'], chapter=self.request.POST['chapter_id'], pk =self.request.POST['assignment_id'])


class MyCourseListView(ListView):
    model = CourseInfo
    template_name = 'teacher_module/mycourses.html'

    paginate_by = 8

    def dispatch(self, request, *args, **kwargs):
        if self.request.GET.get('paginate_by'):
            self.paginate_by = self.request.GET.get('paginate_by')
        return super(MyCourseListView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # courses = InningGroup.objects.filter(Teacher_Code=self.request.user.id,
        #                                      Center_Code=self.request.user.Center_Code)
        # context['courses'] = courses
        # sessions = []
        # if context['courses']:
        #     for course in context['courses']:
        #         # Filtering out only active sessions
        #         session = InningInfo.objects.filter(Groups__id=course.id, End_Date__gt=datetime_now)
        #         sessions += session
        # context['sessions'] = sessions
        #
        # filtered_qs = MyCourseFilter(
        #     self.request.GET,
        #     queryset=courses
        # ).qs
        # filtered_qs = filtered_qs.filter(Course_Code__in=context['object_list'].values_list('pk'))
        courses = self.object_list
        paginator = Paginator(courses, self.paginate_by)
        page = self.request.GET.get('page')
        try:
            response = paginator.page(page)
        except PageNotAnInteger:
            response = paginator.page(1)
        except EmptyPage:
            response = paginator.page(paginator.num_pages)
        context['response'] = response

        return context

    def get_queryset(self):
        qsearch = self.request.user.get_teacher_courses()['courses']
        if '/inactive/' in self.request.path:
            qsearch = [x for x in qsearch if x.Use_Flag is False]
        if '/active/' in self.request.path:
            qsearch = [x for x in qsearch if x.Use_Flag is True]
        courses = []
        query = self.request.GET.get('teacher_mycoursequery')
        if query:
            query = query.strip()
            # qsearch = qsearch.filter(Course_Name__icontains=query)
            for course in qsearch:
                if query in course.Course_Name.lower():
                    courses.append(course)
            if not len(courses):
                messages.error(self.request, 'Sorry no course found! Try with a different keyword')
        else:
            courses = qsearch
        # qsearch = qsearch.order_by("-id")  # you don't need this if you set up your ordering on the model
        return courses


class CourseInfoListView(ListView):
    model = CourseInfo
    template_name = 'teacher_module/courseinfo_list.html'
    paginate_by = 6

    def get_queryset(self):
        qs = self.model.objects.all()

        query = self.request.GET.get('teacher_coursequery')
        if query:
            query = query.strip()
            qs = qs.filter(Course_Name__icontains=query)
            if not len(qs):
                messages.error(self.request, 'Sorry no course found! Try with a different keyword')
        qs = qs.order_by("-id")  # you don't need this if you set up your ordering on the model
        return qs

    # def get_queryset(self):
    #     courses = CourseInfo.objects.filter(
    #         Teacher_Code=self.request.user.id)
    #     if self.request.GET.get('query'):
    #         query = self.request.GET.get('query')
    #         if query:
    #             qs = courses.filter(Course_Name__contains=query)
    #             if not len(qs):
    #                 messages.error(self.request, 'Search not found')
    #         # you don't need this if you set up your ordering on the model
    #         qs = qs.order_by("-id")
    #         return qs
    #     else:
    #         return courses
    # def get_queryset(self):
    #     qs = self.model.objects.all()


class CourseInfoCreateView(CreateView):
    model = CourseInfo
    form_class = CourseInfoForm
    template_name = 'teacher_module/courseinfo_form.html'

    # success_url = reverse_lazy('teacher_courseinfo_list')
    def get_success_url(self, **kwargs):
        return reverse_lazy('teacher_courseinfo_detail', kwargs={'pk': self.object.pk})


class CourseInfoDetailView(TeacherAuthMxnCls, CourseAuthMxnCls, TeacherCourseAuthMxnCls, DetailView):
    model = CourseInfo
    template_name = 'teacher_module/courseinfo_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['chapters'] = ChapterInfo.objects.filter(Course_Code=self.kwargs.get('pk')).order_by('Chapter_No')
        context['surveycount'] = SurveyInfo.objects.filter(Course_Code=self.kwargs.get('pk'))
        context['quizcount'] = Quiz.objects.filter(course_code=self.kwargs.get('pk'), exam_paper=True,
                                                   chapter_code=None)  # exam type
        context['numberOfQuizExclExams'] = Quiz.objects.filter(
            chapter_code__in=context['chapters'].values_list('pk'),
            exam_paper=False, course_code=self.kwargs.get('pk'))
        context['topic'] = Topic.objects.filter(course_associated_with=self.kwargs.get('pk'))
        return context


class CourseInfoUpdateView(CourseAuthMxnCls, TeacherCourseAuthMxnCls, UpdateView):
    model = CourseInfo
    form_class = CourseInfoForm
    template_name = 'teacher_module/courseinfo_form.html'

    def get_form_kwargs(self):
        """
        Returns the keyword arguments for instantiating the form.
        """
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['Course_Code'] = get_object_or_404(CourseInfo, pk=self.kwargs.get('course'))
    #     return context

    def get_success_url(self, **kwargs):
        return reverse_lazy('teacher_courseinfo_detail', kwargs={'pk': self.object.pk})


class ChapterInfoListView(ListView):
    model = ChapterInfo
    template_name = 'teacher_module/chapterinfo_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['Course_Code'] = get_object_or_404(CourseInfo, pk=self.kwargs.get('course'))
        return context


class ChapterInfoCreateView(CreateView):
    model = ChapterInfo
    form_class = ChapterInfoForm
    template_name = 'teacher_module/chapterinfo_form.html'

    def get_form_kwargs(self):
        """
        Returns the keyword arguments for instantiating the form.
        """
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def get_success_url(self, **kwargs):
        return reverse_lazy('teacher_chapterinfo_detail',
                            kwargs={'course': self.object.Course_Code.id, 'pk': self.object.pk})


class ChapterInfoDetailView(TeacherAuthMxnCls, ChapterAuthMxnCls, TeacherChapterAuthMxnCls, DetailView):
    model = ChapterInfo
    template_name = 'teacher_module/chapterinfo_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['assignments'] = AssignmentInfo.objects.filter(Chapter_Code=self.kwargs.get('pk'))
        context['post_quizes'] = Quiz.objects.filter(chapter_code=self.kwargs.get('pk'), post_test=True)
        context['pre_quizes'] = Quiz.objects.filter(chapter_code=self.kwargs.get('pk'), pre_test=True)
        context['datetime'] = timezone.now().replace(microsecond=0)
        course_groups = InningGroup.objects.filter(Course_Code=ChapterInfo.objects.get(
            pk=self.kwargs.get('pk')).Course_Code,
                                                   Teacher_Code=self.request.user.pk)
        context['assigned_session'] = InningInfo.objects.filter(Use_Flag=True,
                                                                Start_Date__lte=datetime_now,
                                                                End_Date__gte=datetime_now,
                                                                Course_Group__in=course_groups)

        return context


def ChapterInfoBuildView(request):
    return render(request, 'teacher_module/coursebuilder.html')


class ChapterInfoUpdateView(ChapterAuthMxnCls, UpdateView):
    model = ChapterInfo
    form_class = ChapterInfoForm
    template_name = 'teacher_module/chapterinfo_form.html'

    def get_form_kwargs(self):
        """
        Returns the keyword arguments for instantiating the form.
        """
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['Course_Code'] = get_object_or_404(CourseInfo, pk=self.kwargs.get('course'))
        return context

    def form_valid(self, form):
        form.save(commit=False)
        # if form.cleaned_data['Start_Date'] == "":
        #     form.instance.Start_Date = None
        # if form.cleaned_data['End_Date'] == "":
        #     form.instance.End_Date = None

        # form.instance.mustreadtime = int(form.cleaned_data['mustreadtime']) * 60
        # form.save()
        return super().form_valid(form)

    def get_success_url(self, **kwargs):
        return reverse_lazy('teacher_chapterinfo_detail',
                            kwargs={'course': self.object.Course_Code.id, 'pk': self.object.pk})


class AssignmentInfoDetailView(AssignmentInfoAuthMxnCls, TeacherAssignmentAuthMxnCls, DetailView):
    model = AssignmentInfo
    template_name = 'teacher_module/assignmentinfo_detail.html'

    def dispatch(self, request, *args, **kwargs):
        if '/teachers' in self.request.path:
            assignmentinfoObj = get_object_or_404(AssignmentInfo, pk=self.kwargs.get('pk'))
            inning_info = InningInfo.objects.filter(Course_Group__Teacher_Code__pk=self.request.user.pk,
                                                    Course_Group__Course_Code__pk=assignmentinfoObj.Course_Code.pk,
                                                    Use_Flag=True,
                                                    End_Date__gt=datetime.now()).distinct().count()
            if inning_info == 0:
                messages.add_message(self.request, messages.ERROR, 'Access Denied. Please Contact Admin.')
                return redirect('teacher_home')
            else:
                return super(AssignmentInfoDetailView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['Questions'] = AssignmentQuestionInfo.objects.filter(Assignment_Code=self.kwargs.get('pk'),
                                                                     )
        context['Course_Code'] = get_object_or_404(CourseInfo, pk=self.kwargs.get('course'))
        context['Chapter_No'] = get_object_or_404(ChapterInfo, pk=self.kwargs.get('chapter'))
        context['datetime'] = datetime.now()

        # ===================== Assignment Answers =============================================

        session_list = []
        inningpk = self.kwargs.get('inningpk') if self.kwargs.get('inningpk') else None

        assignmentinfoObj = get_object_or_404(AssignmentInfo, pk=self.kwargs.get('pk'))
        if '/teachers' in self.request.path:
            inning_info = InningInfo.objects.filter(Course_Group__Teacher_Code__pk=self.request.user.pk,
                                                    Course_Group__Course_Code__pk=assignmentinfoObj.Course_Code.pk,
                                                    Use_Flag=True,
                                                    End_Date__gt=datetime.now()).distinct()
        session_list.append(inning_info)

        if inning_info.count() > 0:
            if inningpk:
                innings = get_object_or_404(inning_info, pk=inningpk)
            else:
                innings = None

        questions = AssignmentQuestionInfo.objects.filter(Assignment_Code=self.kwargs['pk'],
                                                          )
        context['questions'] = questions
        if innings:
            context['Answers'] = AssignAnswerInfo.objects.filter(Question_Code__in=questions,
                                                                 Student_Code__in=innings.Groups.Students.all())
            context['students_list'] = innings.Groups.Students.all()
        else:
            context['Answers'] = AssignAnswerInfo.objects.filter(Question_Code__in=questions)
            context['students_list'] = assignmentinfoObj.Course_Code.get_students_of_this_course()

        context['Assignment'] = assignmentinfoObj
        context['session_list'] = session_list
        context['inning'] = innings
        context['chapter_list'] = assignmentinfoObj.Course_Code.chapterinfos.all()
        course_groups = InningGroup.objects.filter(Course_Code=ChapterInfo.objects.get(
            pk=self.kwargs.get('chapter')).Course_Code,
                                                   Teacher_Code=self.request.user.pk)

        if inningpk:
            context['assigned_session'] = InningInfo.objects.filter(pk=inningpk, Use_Flag=True,
                                                                    Start_Date__lte=datetime_now,
                                                                    End_Date__gte=datetime_now,
                                                                    Course_Group__in=course_groups)
        else:
            context['assigned_session'] = InningInfo.objects.filter(Use_Flag=True,
                                                                    Start_Date__lte=datetime_now,
                                                                    End_Date__gte=datetime_now,
                                                                    Course_Group__in=course_groups)

        # ==================== End of Assignment Answers ========================================

        # context['Assignment_Code'] = get_object_or_404(AssignmentInfo, pk=self.kwargs.get('assignment'))
        return context


class AssignmentInfoDeleteView(DeleteView):
    model = AssignmentInfo

    # Assignment_Code = get_object_or_404(AssignmentInfo, pk=self.kwargs.get('assignment'))

    def post(self, request, *args, **kwargs):

        try:
            # return self.delete(request, *args, **kwargs)
            Obj = AssignmentInfo.objects.get(pk=self.request.POST['assignment_id'])
            Obj.delete()
            return redirect('teacher_chapterinfo_detail', course=request.POST['course_id'],
                            pk=request.POST['chapter_id'])

        except:
            messages.error(request,
                           "Fail")
            return redirect('teacher_assignmentinfo_detail', course=self.request.POST['course_id'],
                            chapter=self.request.POST['chapter_id'], pk=self.request.POST['assignment_id'])
            # return redirect('student_home')
    # success_url = reverse_lazy('assignmentinfo_detail', course=self.request.POST['course_id'], chapter=self.request.POST['chapter_id'], pk =self.request.POST['assignment_id'])


class AssignmentAnswers(AssignmentInfoAuthMxnCls, ListView):
    model = AssignAnswerInfo
    template_name = 'teacher_module/assignment_answers.html'

    def dispatch(self, request, *args, **kwargs):
        if '/teachers' in self.request.path:
            assignmentinfoObj = get_object_or_404(AssignmentInfo, pk=self.kwargs.get('pk'))
            inning_info = InningInfo.objects.filter(Course_Group__Teacher_Code__pk=self.request.user.pk,
                                                    Course_Group__Course_Code__pk=assignmentinfoObj.Course_Code.pk,
                                                    Use_Flag=True,
                                                    End_Date__gt=datetime.now()).distinct().count()
            if inning_info == 0:
                messages.add_message(self.request, messages.ERROR, 'Access Denied. Please Contact Admin.')
                return redirect('teacher_home')
            else:
                return super(AssignmentAnswers, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        session_list = []
        inningpk = self.kwargs.get('inningpk') if self.kwargs.get('inningpk') else None

        assignmentinfoObj = get_object_or_404(AssignmentInfo, pk=self.kwargs.get('pk'))
        if '/teachers' in self.request.path:
            inning_info = InningInfo.objects.filter(Course_Group__Teacher_Code__pk=self.request.user.pk,
                                                    Course_Group__Course_Code__pk=assignmentinfoObj.Course_Code.pk,
                                                    Use_Flag=True,
                                                    End_Date__gt=datetime.now()).distinct()
        session_list.append(inning_info)

        if inning_info.count() > 0:
            if inningpk:
                innings = get_object_or_404(inning_info, pk=inningpk)
            else:
                innings = None

        questions = AssignmentQuestionInfo.objects.filter(Assignment_Code=self.kwargs['pk'],
                                                          )
        context['questions'] = questions
        if innings:
            context['Answers'] = AssignAnswerInfo.objects.filter(Question_Code__in=questions,
                                                                 Student_Code__in=innings.Groups.Students.all())
            context['students_list'] = innings.Groups.Students.all()
        else:
            context['Answers'] = AssignAnswerInfo.objects.filter(Question_Code__in=questions)
            context['students_list'] = assignmentinfoObj.Course_Code.get_students_of_this_course()

        context['Assignment'] = assignmentinfoObj
        context['session_list'] = session_list
        context['inning'] = innings
        context['chapter_list'] = assignmentinfoObj.Course_Code.chapterinfos.all()

        # context['Chapter_No'] = get_object_or_404(ChapterInfo, pk=self.kwargs.get('chapter'))
        # context['Assignment_Code'] = get_object_or_404(AssignmentInfo, pk=self.kwargs.get('assignment'))
        return context


def downloadAssignmentAnswers(request):
    if request.method == "POST":
        list_of_files = request.POST.getlist('list_of_files[]')
        assignment_pk = str(request.POST.get('assignment_id'))
        question_pk = str(request.POST.get('question_id'))
        path = settings.MEDIA_ROOT
        dstfolder = os.path.join('', *[path, 'assignments', assignment_pk, assignment_pk + '_' + question_pk])
        for src in list_of_files:
            # srcfile = os.path.join(path, src)
            if os.path.isfile(os.path.join(path, src)):
                if os.path.exists(dstfolder) and os.path.isdir(dstfolder):
                    shutil.copy(os.path.join(path, src), dstfolder)
                else:
                    os.makedirs(dstfolder)
                    shutil.copy(os.path.join(path, src), dstfolder)
            shutil.make_archive(
                path + '/assignments/' + assignment_pk + '/' + assignment_pk + '_' + question_pk,
                'zip', dstfolder)
        return JsonResponse({
            'link': settings.MEDIA_URL + 'assignments/' + assignment_pk + '/' + assignment_pk + '_' + question_pk + '.zip'
        }, status=200)


def deletedownloadAssignmentAnswers(request):
    assignment_pk = str(request.GET.get('assignment_id'))
    question_pk = str(request.GET.get('question_id'))
    path = settings.MEDIA_ROOT
    dstfolder = os.path.join('', *[path, 'assignments', assignment_pk, assignment_pk + '_' + question_pk])
    if os.path.exists(dstfolder):
        shutil.rmtree(dstfolder)
    return JsonResponse({'message': 'success'}, status=200)


class AssignmentInfoUpdateView(AssignmentInfoAuthMxnCls, TeacherAssignmentAuthMxnCls, UpdateView):
    model = AssignmentInfo
    form_class = AssignmentInfoForm
    template_name = 'teacher_module/assignmentinfo_form.html'

    def get_success_url(self, **kwargs):
        return reverse_lazy('teacher_assignmentinfo_detail',
                            kwargs={'course': self.object.Course_Code.id, 'chapter': self.object.Chapter_Code.id,
                                    'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['Course_Code'] = get_object_or_404(CourseInfo, pk=self.kwargs.get('course'))
        context['Chapter_No'] = get_object_or_404(ChapterInfo, pk=self.kwargs.get('chapter'))
        return context


class MyAssignmentsListView(ListView):
    model = AssignmentInfo
    template_name = 'teacher_module/myassignments.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['currentDate'] = datetime.now()
        context['Group'] = InningGroup.objects.filter(Teacher_Code=self.request.user.id)
        course = []
        context['Assignment'] = []
        context['expiredAssignment'] = []
        context['activeAssignment'] = []
        for c in self.request.user.get_teacher_courses()['courses']:
            course.append(c.id)
        Assignment = []
        expiredAssignment = []
        activeAssignment = []
        for course in course:
            Assignment.append(AssignmentInfo.objects.filter(Course_Code=course))
            expiredAssignment.append(
                AssignmentInfo.objects.filter(Course_Code=course,
                                              Assignment_Deadline__lt=datetime_now))
            activeAssignment.append(
                AssignmentInfo.objects.filter(Course_Code=course,
                                              Assignment_Deadline__gte=datetime_now))
        context['Assignment'].append(Assignment)
        context['activeAssignment'].append(activeAssignment)
        context['expiredAssignment'].append(expiredAssignment)
        return context


def submitStudentscore(request, Answer_id, score):
    if request.method == "POST":

        answerInfo = AssignAnswerInfo.objects.get(pk=Answer_id)
        score = request.POST.get('stu_score')
        if float(score) > answerInfo.Question_Code.Question_Score:
            return HttpResponse("failure", status=500)
        answerInfo.Assignment_Score = score
        if request.POST.get('assignment_feedback'):
            answerInfo.Assignment_Feedback = request.POST.get('assignment_feedback')

            # Notification for students after teacher gives feedback on question
            student_description = '{} has provided feedback on Question "{}" of assignment "{}".'.format(
                request.user,
                answerInfo.Question_Code.Question_Title,
                answerInfo.Question_Code.Assignment_Code.Assignment_Topic,
            )
            notify.send(
                sender=request.user,
                recipient=answerInfo.Student_Code,
                verb='commented',
                description=student_description,
                action_object=answerInfo.Question_Code.Assignment_Code,
                is_sent=True
            )
            # ------------------------------------------------------------------------------------------

        answerInfo.save()

        # Notification for students after teacher gives score on question
        student_description = '{} score has been given to Question "{}" of assignment "{}".'.format(
            answerInfo.Assignment_Score,
            answerInfo.Question_Code.Question_Title,
            answerInfo.Question_Code.Assignment_Code.Assignment_Topic,
        )
        notify.send(
            sender=request.user,
            recipient=answerInfo.Student_Code,
            verb='marked',
            description=student_description,
            action_object=answerInfo.Question_Code.Assignment_Code,
            is_sent=True
        )
        # ------------------------------------------------------------------------------------------
        return HttpResponse("success")
    else:
        return HttpResponse("You are not allowed to do this")


def ProfileView(request):
    return render(request, 'teacher_module/profile.html')


class PasswordChangeView(PasswordContextMixin, FormView):
    form_class = PasswordChangeForm
    success_url = reverse_lazy('teacher_user_profile')
    title = _('Password change')

    @method_decorator(sensitive_post_parameters())
    @method_decorator(csrf_protect)
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.save()
        # Updating the password logs out all other sessions for the user
        # except the current one.
        update_session_auth_hash(self.request, form.user)

        messages.success(self.request,
                         'Your password was successfully updated! You can login with your new credentials')
        return super().form_valid(form)


def makequery(request):
    # model=SurveyInfo
    Course = CourseInfo.objects.all()
    Session = InningInfo.objects.all()
    return render(request, 'teacher_module/makequery.html', {
        'courses': Course,
        'sessions': Session
    })


# class question_teachers(ListView):
#     model = SurveyInfo

class SurveyInfoListView(ListView):
    model = SurveyInfo
    template_name = 'teacher_module/survey/question_teachers.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['currentDate'] = datetime.now().date()
        context['categories'] = CategoryInfo.objects.all()
        context['questions'] = QuestionInfo.objects.filter(
            Survey_Code=self.kwargs.get('pk')).order_by('pk')

        context['options'] = OptionInfo.objects.all()
        context['submit'] = SubmitSurvey.objects.all()

        # context['categoryName'] = CategoryInfo.objects.values_list('Category_Name')

        # context['surveyForm'] = {'categoryName': list(categoryName)}
        # context['categoryName'] = CategoryInfo.objects.values_list('Category_Name')
        # context['surveyForm'] = serializers.serialize('json', list(categoryName), fields=('Category_Name'))

        return context


class TeacherSurveyInfo_ajax(AjaxableResponseMixin, CreateView):
    model = SurveyInfo
    form_class = SurveyInfoForm
    template_name = 'ajax/surveyInfoAddSurvey_ajax2.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['questioninfo_formset'] = QuestionInfoFormset(self.request.POST, prefix='questioninfo')  # MCQ
            context['questionansinfo_formset'] = QuestionAnsInfoFormset(self.request.POST,
                                                                        prefix='questionansinfo')  # SAQ
        else:
            context['questioninfo_formset'] = QuestionInfoFormset(prefix='questioninfo')
            context['questionansinfo_formset'] = QuestionAnsInfoFormset(prefix='questionansinfo')
            context['category_name'] = self.request.GET['category_name']
            if context['category_name'].lower() == 'live':
                context['course_code'] = self.request.GET['course_code']

        return context

    def form_valid(self, form):

        if form.is_valid():
            self.object = form.save(commit=False)
            if self.request.GET['category_name'].lower() == "system":
                self.object.Center_Code = None
            else:
                self.object.Center_Code = self.request.user.Center_Code
            self.object.Added_By = self.request.user
            if self.request.GET['category_name'].lower() == "live":
                self.object.Course_Code = get_object_or_404(CourseInfo, id=self.request.GET['course_code'])
                self.object.Survey_Live = True
                self.object.End_Date = timezone.now() + timedelta(seconds=int(self.request.POST["End_Time"]))
                self.object.save()
            super().form_valid(form)
        context = self.get_context_data()
        qn = context['questioninfo_formset']
        qna = context['questionansinfo_formset']
        with transaction.atomic():
            for f in qn:
                print("is changed: ", f.has_changed())
            if qn.is_valid():
                qn.instance = self.object
                qn.save()
            else:
                print("qn is invalid", qn.errors)
            if qna.is_valid():
                qna.instance = self.object
                qna.save()
            else:
                print("qna is invalid", qna.errors)
        response = {'url': self.request.build_absolute_uri(reverse('surveyinfo_detail', kwargs={'pk': self.object.id})),
                    'teacher_url': self.request.build_absolute_uri(
                        reverse('surveyinfodetail', kwargs={'pk': self.object.id})),

                    'quiz_id': self.object.id,
                    'student_url': self.request.build_absolute_uri(
                        reverse('questions_student_detail', kwargs={'pk': self.object.id}))}
        return JsonResponse(response)

    def get_form_kwargs(self):
        kwargs = super(TeacherSurveyInfo_ajax, self).get_form_kwargs()
        kwargs.update({'request': self.request})
        return kwargs


def polls_teachers(request):
    return render(request, 'teacher_module/survey/surveyinfodetail.html')


class AjaxableResponseMixin:
    """
    Mixin to add AJAX support to a form.
    Must be used with an object-based FormView (e.g. CreateView)
    """

    def form_invalid(self, form):
        response = super().form_invalid(form)
        if self.request.is_ajax():
            return JsonResponse(form.errors, status=400)
        else:
            return response

    def form_valid(self, form):
        # We make sure to call the parent's form_valid() method because
        # it might do some processing (in the case of CreateView, it will
        # call form.save() for example).
        response = super().form_valid(form)
        if self.request.is_ajax():
            data = {
                'pk': self.object.pk,
            }
            return JsonResponse(data)
        else:
            return response


class QuizCreateView(CreatePopupMixin, CreateView):
    # template_name = 'quiz/test_temp.html'
    model = Quiz
    # fields = ['title']
    form_class = QuizForm
    success_url = reverse_lazy('teacher_quiz_list')


class QuizListView(ListView):
    model = Quiz
    template_name = 'teacher_quiz/quiz_list.html'

    def get_queryset(self):
        queryset = super(QuizListView, self).get_queryset()
        innings_Course_Code = InningGroup.objects.filter(Teacher_Code=self.request.user.id).values('Course_Code')
        return queryset.filter(
            cent_code=self.request.user.Center_Code,
            course_code__in=innings_Course_Code
        )


class QuizUpdateView(QuizInfoAuthMxnCls, UpdateView):
    model = Quiz
    form_class = QuizForm


class UpdateQuizBasicInfo(QuizInfoAuthMxnCls, UpdateView):
    model = Quiz
    form_class = QuizBasicInfoForm
    template_name = 'teacher_quiz/quiz_update_basic_info.html'

    def get_form_kwargs(self):
        default_kwargs = super().get_form_kwargs()
        default_kwargs['current_obj'] = self.object
        return default_kwargs

    def get_success_url(self):
        return reverse(
            'teacher_quiz_detail',
            kwargs={'pk': self.object.pk},
        )


class QuizDetailView(QuizInfoAuthMxnCls, DetailView):
    model = Quiz
    slug_field = 'url'
    template_name = 'teacher_quiz/quiz_detail.html'

    # def get(self, request, *args, **kwargs):
    #     self.object = self.get_object()
    #
    #     if self.object.draft and not request.user.has_perm('quiz.change_quiz'):
    #         raise PermissionDenied
    #
    #     context = self.get_context_data(object=self.object)
    #     return self.render_to_response(context)


def QuizDeleteView(request, pk):
    Quiz.objects.filter(pk=pk).delete()
    return redirect("teacher_quiz_list")


class CategoriesListView(ListView):
    model = CourseInfo


class QuizUserProgressView(TemplateView):
    template_name = 'progress.html'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(QuizUserProgressView, self) \
            .dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(QuizUserProgressView, self).get_context_data(**kwargs)
        progress, c = Progress.objects.get_or_create(user=self.request.user)
        context['cat_scores'] = progress.list_all_cat_scores
        context['exams'] = progress.show_exams()
        return context


class QuizMarkingList(TeacherAuthMxnCls, QuizMarkerMixin, ListView):
    model = Quiz
    template_name = 'teacher_quiz/marking_list.html'

    def get_context_data(self, **kwargs):
        context = super(QuizMarkingList, self).get_context_data(**kwargs)
        innings_Course_Code = InningGroup.objects.filter(Teacher_Code=self.request.user.id).values('Course_Code')
        context['quiz_list'] = context['quiz_list'].filter(
            cent_code=self.request.user.Center_Code,
            course_code__in=innings_Course_Code
        )
        for q in context['quiz_list']:
            sittings = Sitting.objects.filter(quiz=q)
            if not sittings:
                context['quiz_list'] = context['quiz_list'].exclude(id=q.id)

        for q in context['quiz_list']:
            sittings = Sitting.objects.filter(quiz=q)
            q.count = sittings.count()
            q.complete_count = sittings.filter(complete=True).count()
            q.student_count = sittings.annotate(Count('user', distinct=True)).count()
            q.student_complete_count = sittings.filter(complete=True).annotate(Count('user', distinct=True)).count()

        return context


class QuizMarking(TeacherAuthMxnCls, QuizMarkerMixin, SittingFilterTitleMixin, ListView):
    model = Sitting
    template_name = 'teacher_quiz/sitting_list.html'

    def get_queryset(self):
        queryset = super(QuizMarking, self).get_queryset().filter(complete=True)
        quiz_id = int(self.kwargs['quiz_id'])
        queryset = queryset.filter(quiz__id=quiz_id)

        user_filter = self.request.GET.get('user_filter')
        if user_filter:
            queryset = queryset.filter(user__username__icontains=user_filter)

        innings_Course_Code = InningGroup.objects.filter(Teacher_Code=self.request.user.id).values('Course_Code')
        my_quiz = Quiz.objects.filter(course_code__in=innings_Course_Code)
        queryset = queryset.filter(quiz__in=my_quiz)

        return queryset

    def get_context_data(self, **kwargs):
        context = super(QuizMarking, self).get_context_data(**kwargs)
        quiz_id = int(self.kwargs['quiz_id'])
        context['quiz'] = Quiz.objects.get(id=quiz_id)
        return context


class QuizMarkingDetail(TeacherAuthMxnCls, QuizMarkerMixin, DetailView):
    model = Sitting
    template_name = 'teacher_quiz/sitting_detail.html'

    def dispatch(self, *args, **kwargs):
        # Check if the teacher is allocated to course of not
        if TeacherCourseAuth(self.request, get_object_or_404(Sitting, pk=kwargs.get('pk')).quiz.course_code.pk) != 1:
            return redirect('login')
        return super(QuizMarkingDetail, self).dispatch(self.request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        sitting = self.get_object()

        q_to_toggle = request.POST.get('saq_id', None)
        if q_to_toggle:
            q = Question.objects.get_subclass(id=int(q_to_toggle))
            indx = [int(n) for n in sitting.question_order.split(',') if n].index(q.id)
            print(request.POST['new_score'], "new_score")
            print(indx, "index")
            score_list = [s for s in sitting.score_list.split(',') if s]
            score_list[indx] = request.POST.get('new_score', 0)
            sitting.score_list = ','.join(list(map(str, score_list)))
            print(sitting.score_list, "score_list_update")
            sitting.save()
            # if int(q_to_toggle) in sitting.get_incorrect_questions:
            #     sitting.remove_incorrect_question(q)
            # else:
            #     sitting.add_incorrect_question(q)

        return self.get(request)

    def get_context_data(self, **kwargs):
        context = super(QuizMarkingDetail, self).get_context_data(**kwargs)
        context['questions'] = context['sitting'].get_questions(with_answers=True)
        total = 0
        total_score_obtained = 0
        for q in context['questions']:
            i = [int(n) for n in context['sitting'].question_order.split(',') if n].index(q.id)
            # score_list = context['sitting'].score_list.replace("not_graded", "0")
            try:
                score = [s for s in context['sitting'].score_list.split(',') if s][i]
            except:
                score = 'not_graded'
            q.score_obtained = score
            total += q.score
            if score != "not_graded":
                total_score_obtained += float(score)
        context['total_score_obtained'] = total_score_obtained
        context['total'] = total

        return context


def anon_session_score(session, to_add=0, possible=0):
    """
    Returns the session score for non-signed in users.
    If number passed in then add this to the running total and
    return session score.

    examples:
        anon_session_score(1, 1) will add 1 out of a possible 1
        anon_session_score(0, 2) will add 0 out of a possible 2
        x, y = anon_session_score() will return the session score
                                    without modification

    Left this as an individual function for unit testing
    """
    if "session_score" not in session:
        session["session_score"], session["session_score_possible"] = 0, 0

    if possible > 0:
        session["session_score"] += to_add
        session["session_score_possible"] += possible

    return session["session_score"], session["session_score_possible"]


class QuestionCreateView(CreateView):
    model = Question
    form_class = QuestionForm


# ------------------------- MC_Question Views------------------


class MCQuestionListView(ListView):
    model = MCQuestion
    template_name = 'teacher_module/mcquestion_list.html'


class MCQuestionCreateView(AjaxableResponseMixin, CreateView):
    model = MCQuestion
    form_class = MCQuestionForm
    # success_url = reverse_lazy('quiz_create')
    template_name = 'ajax/mcquestion_form_ajax.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['answers_formset'] = AnsFormset(self.request.POST)
        else:
            context['answers_formset'] = AnsFormset()
            context['course_from_quiz'] = self.request.GET["course_from_quiz"]
        return context

    def form_valid(self, form):
        vform = super().form_valid(form)
        context = self.get_context_data()
        ans = context['answers_formset']
        with transaction.atomic():
            if ans.is_valid():
                ans.instance = self.object
                ans.save()
        new_mcq = {}
        new_mcq['new_mcq_id'] = self.object.id
        new_mcq['new_mcq_content'] = self.object.content
        return JsonResponse(new_mcq)


class MCQuestionUpdateView(UpdateView):
    model = MCQuestion
    form_class = MCQuestionForm
    success_url = reverse_lazy('teacher_quiz_create')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['answers_formset'] = AnsFormset(self.request.POST, instance=self.object)
        else:
            context['answers_formset'] = AnsFormset(instance=self.object)
        return context

    def form_valid(self, form):
        vform = super().form_valid(form)
        context = self.get_context_data()
        ans = context['answers_formset']
        with transaction.atomic():
            if ans.is_valid():
                ans.instance = self.object
                ans.save()
        return vform


class MCQuestionDetailView(DetailView):
    model = MCQuestion
    template_name = 'teacher_module/mcquestion_detail.html'


def MCQuestionDeleteView(request, pk):
    MCQuestion.objects.filter(pk=pk).delete()
    return redirect("teacher_mcquestion_list")


class MCQuestionCreateFromQuiz(CreateView):
    model = MCQuestion
    fields = ['figure', 'content', 'explanation', 'answer_order']
    template_name = 'teacher_module/mcquestion_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['answers_formset'] = AnsFormset(self.request.POST)
        else:
            context['answers_formset'] = AnsFormset()
        return context

    def form_valid(self, form):
        related_quiz = Quiz.objects.get(id=self.kwargs['quiz_id'])
        if form.is_valid():
            self.object = form.save()
        self.object.cent_code = related_quiz.cent_code
        self.object.course_code = related_quiz.course_code
        vform = super().form_valid(form)
        related_quiz.mcquestion.add(self.object)
        context = self.get_context_data()
        ans = context['answers_formset']
        with transaction.atomic():
            if ans.is_valid():
                ans.instance = self.object
                ans.save()
        return vform

    def get_success_url(self, **kwargs):
        return reverse(
            'teacher_quiz_detail',
            kwargs={'pk': self.kwargs['quiz_id']},
        )


class MCQuestionUpdateFromQuiz(UpdateView):
    model = MCQuestion
    fields = ['figure', 'content', 'explanation', 'answer_order']
    template_name = 'teacher_module/mcquestion_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['answers_formset'] = AnsFormset(self.request.POST, instance=self.object)
        else:
            context['answers_formset'] = AnsFormset(instance=self.object)
        return context

    def form_valid(self, form):
        related_quiz = Quiz.objects.get(id=self.kwargs['quiz_id'])
        if form.is_valid():
            self.object = form.save()
        self.object.cent_code = related_quiz.cent_code
        self.object.course_code = related_quiz.course_code
        vform = super().form_valid(form)
        related_quiz.mcquestion.add(self.object)
        context = self.get_context_data()
        ans = context['answers_formset']
        with transaction.atomic():
            if ans.is_valid():
                ans.instance = self.object
                ans.save()
        return vform

    def get_success_url(self, **kwargs):
        return reverse(
            'teacher_quiz_detail',
            kwargs={'pk': self.kwargs['quiz_id']},
        )


# -------------------------_Question Views------------------

class TFQuestionListView(ListView):
    model = TF_Question
    template_name = 'teacher_module/tf_question_list.html'


class TFQuestionCreateView(AjaxableResponseMixin, CreateView):
    model = TF_Question
    form_class = TFQuestionForm
    # success_url = reverse_lazy('quiz_create')
    template_name = 'ajax/tfquestion_form_ajax.html'

    def form_valid(self, form):
        vform = super().form_valid(form)
        new_tfq = {}
        new_tfq['new_tfq_id'] = self.object.id
        new_tfq['new_tfq_content'] = self.object.content
        return JsonResponse(new_tfq)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.GET:
            context['course_from_quiz'] = self.request.GET["course_from_quiz"]
        return context


class TFQuestionCreateFromQuiz(CreateView):
    model = TF_Question
    fields = ['figure', 'content', 'explanation', 'correct']
    template_name = 'teacher_module/tf_question_form.html'

    def form_valid(self, form):
        related_quiz = Quiz.objects.get(id=self.kwargs['quiz_id'])
        if form.is_valid():
            self.object = form.save()
        self.object.cent_code = related_quiz.cent_code
        self.object.course_code = related_quiz.course_code
        vform = super().form_valid(form)
        related_quiz.tfquestion.add(self.object)
        return vform

    def get_success_url(self, **kwargs):
        return reverse(
            'teacher_quiz_detail',
            kwargs={'pk': self.kwargs['quiz_id']},
        )


class TFQuestionUpdateFromQuiz(UpdateView):
    model = TF_Question
    fields = ['figure', 'content', 'explanation', 'correct']
    template_name = 'teacher_module/tf_question_form.html'

    def form_valid(self, form):
        related_quiz = Quiz.objects.get(id=self.kwargs['quiz_id'])
        if form.is_valid():
            self.object = form.save()
        self.object.cent_code = related_quiz.cent_code
        self.object.course_code = related_quiz.course_code
        vform = super().form_valid(form)
        related_quiz.tfquestion.add(self.object)
        return vform

    def get_success_url(self, **kwargs):
        return reverse(
            'teacher_quiz_detail',
            kwargs={'pk': self.kwargs['quiz_id']},
        )


class TFQuestionUpdateView(UpdateView):
    model = TF_Question
    form_class = TFQuestionForm
    success_url = reverse_lazy('teacher_quiz_create')
    template_name = 'teacher_module/tf_question_form.html'


class TFQuestionDetailView(DetailView):
    model = TF_Question
    template_name = 'teacher_module/tf_question_detail.html'


def TFQuestionDeleteView(request, pk):
    TF_Question.objects.filter(pk=pk).delete()
    return redirect("teacher_tfquestion_list")


# ------------------------- SA_Question Views------------------

class SAQuestionListView(ListView):
    model = SA_Question
    template_name = 'teacher_module/sa_question_list.html'


class SAQuestionCreateView(AjaxableResponseMixin, CreateView):
    model = SA_Question
    form_class = SAQuestionForm
    # success_url = reverse_lazy('quiz_create')
    template_name = 'ajax/saquestion_form_ajax.html'

    def form_valid(self, form):
        vform = super().form_valid(form)
        new_saq = {}
        new_saq['new_saq_id'] = self.object.id
        new_saq['new_Saq_content'] = self.object.content
        return JsonResponse(new_saq)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.GET:
            context['course_from_quiz'] = self.request.GET["course_from_quiz"]
        return context


class SAQuestionCreateFromQuiz(CreateView):
    model = SA_Question
    fields = ['figure', 'content', 'explanation']
    template_name = 'teacher_module/sa_question_form.html'

    def form_valid(self, form):
        related_quiz = Quiz.objects.get(id=self.kwargs['quiz_id'])
        if form.is_valid():
            self.object = form.save()
        self.object.cent_code = related_quiz.cent_code
        self.object.course_code = related_quiz.course_code
        vform = super().form_valid(form)
        related_quiz.saquestion.add(self.object)
        return vform

    def get_success_url(self, **kwargs):
        return reverse(
            'teacher_quiz_detail',
            kwargs={'pk': self.kwargs['quiz_id']},
        )


class SAQuestionUpdateFromQuiz(UpdateView):
    model = SA_Question
    fields = ['figure', 'content', 'explanation']
    template_name = 'teacher_module/sa_question_form.html'

    def form_valid(self, form):
        related_quiz = Quiz.objects.get(id=self.kwargs['quiz_id'])
        if form.is_valid():
            self.object = form.save()
        self.object.cent_code = related_quiz.cent_code
        self.object.course_code = related_quiz.course_code
        vform = super().form_valid(form)
        related_quiz.saquestion.add(self.object)
        return vform

    def get_success_url(self, **kwargs):
        return reverse(
            'teacher_quiz_detail',
            kwargs={'pk': self.kwargs['quiz_id']},
        )


class SAQuestionUpdateView(UpdateView):
    model = SA_Question
    form_class = SAQuestionForm
    success_url = reverse_lazy('teacher_quiz_create')
    template_name = 'teacher_module/sa_question_form.html'


class SAQuestionDetailView(DetailView):
    model = SA_Question
    template_name = 'teacher_module/sa_question_detail.html'


def SAQuestionDeleteView(request, pk):
    SA_Question.objects.filter(pk=pk).delete()
    return redirect("teacher_essayquestion_list")


FORMS = [("form1", QuizForm1),
         ("form2", QuizForm2),
         ("form3", QuizForm3)]

TEMPLATES = {"form1": "teacher_quiz/step1.html",
             "form2": "teacher_quiz/step2.html",
             "form3": "teacher_quiz/step3.html"}


class QuizCreateWizard(SessionWizardView):
    form_list = FORMS

    def get_template_names(self):
        return [TEMPLATES[self.steps.current]]

    def done(self, form_list, **kwargs):
        form_dict = self.get_all_cleaned_data()
        my_quiz = Quiz()
        mcq = form_dict.pop('mcquestion')
        tfq = form_dict.pop('tfquestion')
        saq = form_dict.pop('saquestion')
        for k, v in form_dict.items():
            setattr(my_quiz, k, v)
        my_quiz.save()
        my_quiz.url = str(my_quiz.title) + str(my_quiz.id)
        my_quiz.cent_code = self.request.user.Center_Code
        my_quiz.save()
        my_quiz.mcquestion.add(*mcq)
        my_quiz.tfquestion.add(*tfq)
        my_quiz.saquestion.add(*saq)
        return redirect('teacher_quiz_list')

    def get_form(self, step=None, data=None, files=None):
        form = super().get_form(step, data, files)

        # determine the step if not given
        if step is None:
            step = self.steps.current

        if step == 'form1':
            innings_Course_Code = InningGroup.objects.filter(Teacher_Code=self.request.user.id).values('Course_Code')
            form.fields["course_code"].queryset = CourseInfo.objects.filter(
                Center_Code=self.request.user.Center_Code,
                id__in=innings_Course_Code
            )

        if step == 'form2':
            step1_data = self.get_cleaned_data_for_step('form1')
            step1_course = step1_data['course_code']
            form.fields["chapter_code"].queryset = ChapterInfo.objects.filter(Course_Code=step1_course)

        if step == 'form3':
            step1_data = self.get_cleaned_data_for_step('form1')
            form.fields["mcquestion"].queryset = MCQuestion.objects.filter(course_code=step1_data['course_code'])

        return form

    def get_context_data(self, form, **kwargs):
        context = super().get_context_data(form=form, **kwargs)
        if self.steps.current == 'form3':
            step1_data = self.get_cleaned_data_for_step('form1')
            step1_course = step1_data['course_code']
            context.update({'course_from_quiz': step1_course})
        return context


class teacherSurveyFilterCategory(ListView):
    model = SurveyInfo
    template_name = 'survey/common/surveyinfo_expireView.html'

    paginate_by = 6

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.GET = None

    def get_queryset(self):
        # try:
        category_name = self.request.GET['category_name'].lower()
        date_filter = self.request.GET['date_filter'].lower()
        # teacher related data
        teacher_course_group = InningGroup.objects.filter(Teacher_Code=self.request.user.id)
        teacher_session = InningInfo.objects.filter(Course_Group__in=teacher_course_group).distinct()
        teacher_course = teacher_course_group.values('Course_Code')

        # Predefined category name "general, session, course, system"
        general_survey = SurveyInfo.objects.filter(Category_Code__Category_Name__iexact="general",
                                                   Center_Code=self.request.user.Center_Code)
        session_survey = SurveyInfo.objects.filter(Category_Code__Category_Name__iexact="session",
                                                   Session_Code__in=teacher_session)
        course_survey = SurveyInfo.objects.filter(Category_Code__Category_Name__iexact="course",
                                                  Course_Code__in=teacher_course)
        system_survey = SurveyInfo.objects.filter(Center_Code=None)

        my_queryset = None
        if category_name == "all_survey":
            my_queryset = general_survey | session_survey | course_survey | system_survey
        else:
            if category_name == "general":
                my_queryset = general_survey
            elif category_name == "session":
                my_queryset = session_survey
            elif category_name == "course":
                my_queryset = course_survey
            elif category_name == "system":
                my_queryset = system_survey

        if date_filter == "active":
            my_queryset = my_queryset.filter(End_Date__gt=timezone.now())
            print(date_filter, "query", len(my_queryset))
        elif date_filter == "expire":
            my_queryset = my_queryset.filter(End_Date__lte=timezone.now())
            print(date_filter, "query", len(my_queryset))
        # elif date_filter == "live":
        #     my_queryset = my_queryset.filter(End_Date__gt=timezone.now(), Survey_Live=True)
        #     print(date_filter, "query", len(my_queryset))

        return my_queryset

    # except:
    #     return None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['currentDate'] = datetime.now()
        context['category_name'] = self.request.GET['category_name'].lower()
        context['date_filter'] = self.request.GET['date_filter'].lower()
        return context


class TeacherSurveyInfoDetailView(SurveyInfoAuthMxnCls, DetailView):
    model = SurveyInfo
    template_name = 'teacher_module/survey/surveyinfodetail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['questions'] = QuestionInfo.objects.filter(
            Survey_Code=self.kwargs.get('pk')).order_by('pk')
        context['options'] = OptionInfo.objects.filter(Question_Code__in=context['questions']).order_by('pk')
        context['submit'] = SubmitSurvey.objects.filter(Survey_Code=self.kwargs.get('pk')).count()
        if self.object.Retaken_From:
            context['history'] = SurveyInfo.objects.filter(id=self.object.Retaken_From)
            context['history'] |= SurveyInfo.objects.filter(Retaken_From=self.object.Retaken_From).order_by(
                'Version_No')

        else:
            context['history'] = SurveyInfo.objects.filter(id=self.object.id)
            context['history'] |= SurveyInfo.objects.filter(Retaken_From=self.object.id).order_by(
                'Version_No')
        return context


# ___________________________________________________FORUM____________________________________

class Index(LoginRequiredMixin, ListView):
    model = Thread
    template_name = 'teacher_module/teacher_forum/forumIndex.html'
    context_object_name = 'threads'

    # def get_queryset(self):
    #     nodegroups = NodeGroup.objects.all()
    #     threadqueryset = Thread.objects.none()
    #     for ng in nodegroups:
    #         topics = Topic.objects.filter(node_group=ng.pk).filter(id__in=Topic_related_to_user(self.request))
    #         for topic in topics:
    #             threads = Thread.objects.visible().filter(topic=topic.pk).order_by('pub_date').filter(
    #                 topic_id__in=Topic_related_to_user(self.request))[:4]
    #             threadqueryset |= threads
    #     return threadqueryset

    def get_context_data(self, **kwargs):
        context = super(ListView, self).get_context_data(**kwargs)
        nodegroups = NodeGroup.objects.all()
        threads = []

        for ng in nodegroups:
            thread_counter = 0
            topics = Topic_related_to_user(self.request, node_group=ng)
            # topics = Topic.objects.filter(node_group=ng.pk, center_associated_with= self.request.user.Center_Code) | Topic.objects.filter(node_group=ng.pk, center_associated_with__isnull= True)
            for topic in topics:
                thread_counter += topic.threads_count
            if thread_counter == 0:
                nodegroups = nodegroups.exclude(pk=ng.pk)
            else:
                thread = Thread.objects.filter(topic_id__in=topics).order_by('-pub_date')[:4]
                threads += thread

        context['nodegroups'] = nodegroups
        context['threads'] = threads
        context['panel_title'] = _('New Threads')
        context['title'] = _('Index')
        context['topics'] = Topic.objects.all().filter(id__in=Topic_related_to_user(self.request))
        context['show_order'] = True
        context['get_top_thread_keywords'] = get_top_thread_keywords(self.request, 10)
        return context


@login_required
def create_thread(request, topic_pk=None, nodegroup_pk=None):
    topic = None
    node_group = NodeGroup.objects.all()
    topics = Topic.objects.all()
    fixed_nodegroup = NodeGroup.objects.filter(pk=nodegroup_pk)
    if topic_pk:
        topic = Topic.objects.get(pk=topic_pk)
    if nodegroup_pk:
        topics = topics.filter(node_group=nodegroup_pk)
    topics = topics.filter(id__in=Topic_related_to_user(request))
    if request.method == 'POST':
        form = ThreadForm(request.POST, user=request.user)
        if form.is_valid():
            t = form.save()
            return HttpResponseRedirect(reverse('teacher_thread', kwargs={'pk': t.pk}))
    else:
        form = ThreadForm(user=request.user)

    return render(request, 'teacher_module/teacher_forum/create_thread.html',
                  {'form': form, 'node_group': node_group, 'title': ('Create Thread'), 'topic': topic,
                   'fixed_nodegroup': fixed_nodegroup, 'topics': topics})


def create_topic(request, teacher_nodegroup_pk=None):
    node_group = NodeGroup.objects.filter(pk=teacher_nodegroup_pk)
    if request.method == 'POST':
        form = TopicForm(request.POST, user=request.user)
        if form.is_valid():
            t = form.save()
            return HttpResponseRedirect(reverse('teacher_topic', kwargs={'pk': t.pk}))
    else:
        form = TopicForm()

    return render(request, 'teacher_module/teacher_forum/create_topic.html',
                  {'form': form, 'title': ('Create Topic'), 'node_group': node_group})


def get_default_ordering():
    return getattr(
        settings,
        "forum_DEFAULT_THREAD_ORDERING",
        "-last_replied"
    )


def get_thread_ordering(request):
    query_order = request.GET.get("order", "")
    if query_order in ["-last_replied", "last_replied", "pub_date", "-pub_date"]:
        return query_order
    return get_default_ordering()


class SearchView(ListView):
    model = Thread
    paginate_by = 10
    template_name = 'teacher_module/teacher_forum/search.html'
    context_object_name = 'threads'

    def get_queryset(self):
        keywords = self.kwargs.get('keyword')
        query = get_query(keywords, ['title'])
        return Thread.objects.filter(
            query
        ).select_related(
            'user', 'topic'
        ).prefetch_related(
            'user__forum_avatar'
        ).order_by(
            get_thread_ordering(self.request)
        ).filter(topic_id__in=Topic_related_to_user(self.request))[:100]

    def get_context_data(self, **kwargs):
        context = super(ListView, self).get_context_data(**kwargs)
        context['title'] = context['panel_title'] = _(
            'Search: ') + self.kwargs.get('keyword')
        context['show_order'] = True
        context['keyword'] = self.kwargs.get('keyword')
        return context


def search_redirect(request):
    if request.method == 'GET':
        keyword = request.GET.get('keyword')
        return HttpResponseRedirect(reverse('teacher_search', kwargs={'keyword': keyword}))
    else:
        return HttpResponseForbidden('Post you cannot')


class NodeGroupView(ListView):
    model = Topic
    template_name = 'teacher_module/teacher_forum/nodegroup.html'
    context_object_name = 'topics'

    def get_queryset(self):
        return Topic.objects.filter(
            node_group__id=self.kwargs.get('pk')
        ).select_related(
            'user', 'node_group'
        ).prefetch_related(
            'user__forum_avatar'
        ).filter(id__in=Topic_related_to_user(self.request))

    def get_context_data(self, **kwargs):
        topics = Topic.objects.filter(node_group__id=self.kwargs.get('pk')).filter(
            id__in=Topic_related_to_user(self.request))

        latest_threads = []
        for topic in topics:
            reply_count = 0
            try:
                thread = Thread.objects.filter(
                    topic=topic.pk).order_by('pub_date')[0]
                reply_count = Post.objects.filter(thread=thread.pk).count()

            except:
                thread = None
            latest_threads.append([topic, thread, reply_count])
        context = super(ListView, self).get_context_data(**kwargs)
        context['node_group'] = nodegroup = NodeGroup.objects.get(
            pk=self.kwargs.get('pk'))
        context['title'] = context['panel_title'] = nodegroup.title
        context['show_order'] = True
        context['latest_thread_for_topics'] = latest_threads
        return context


class ThreadView(ListView):
    model = Post
    paginate_by = 15
    template_name = 'teacher_module/teacher_forum/thread.html'
    context_object_name = 'posts'

    def get_queryset(self):
        return Post.objects.filter(
            thread_id=self.kwargs.get('pk')
        ).select_related(
            'user'
        ).prefetch_related(
            'user__forum_avatar'
        ).order_by('pub_date')[:5]

    def get_context_data(self, **kwargs):
        context = super(ListView, self).get_context_data(**kwargs)
        current = Thread.objects.get(pk=self.kwargs.get('pk'))
        current.increase_view_count()
        context['thread'] = current
        context['title'] = context['thread'].title
        context['topic'] = context['thread'].topic
        context['form'] = ReplyForm()
        context['total_reply_count'] = Post.objects.filter(
            thread_id=self.kwargs.get('pk')
        ).select_related(
            'user'
        ).prefetch_related(
            'user__forum_avatar'
        ).order_by('pub_date').count()

        return context

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        current = Thread.objects.visible().get(pk=self.kwargs.get('pk'))
        if current.closed:
            return HttpResponseForbidden("Thread closed")
        thread_id = self.kwargs.get('pk')
        form = ReplyForm(
            request.POST,
            user=request.user,
            thread_id=thread_id
        )
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(
                reverse('teacher_thread', kwargs={'pk': thread_id})
            )


def ThreadList_LoadMoreViewAjax(request, pk, count):
    return render(request, 'ForumInclude/LoadMoreAjax.html', {
        'MoreReply': Post.objects.filter(
            thread_id=pk
        ).select_related(
            'user'
        ).prefetch_related(
            'user__forum_avatar'
        ).order_by('pub_date')[5 * count:(1 + count) * 5]

    })


class TopicView(ListView):
    model = Thread
    paginate_by = 20
    template_name = 'teacher_module/teacher_forum/topic.html'
    context_object_name = 'threads'

    def get_queryset(self):
        return Thread.objects.visible().filter(
            topic__id=self.kwargs.get('pk')
        ).select_related(
            'user', 'topic'
        ).prefetch_related(
            'user__forum_avatar'
        ).order_by(
            *['order', get_thread_ordering(self.request)]
        )

    def get_context_data(self, **kwargs):
        context = super(ListView, self).get_context_data(**kwargs)
        context['topic'] = topic = Topic.objects.get(pk=self.kwargs.get('pk'))
        context['title'] = context['panel_title'] = topic.title
        context['show_order'] = True
        return context


def user_info(request, pk):
    u = User.objects.get(pk=pk)
    return render(request, 'teacher_module/teacher_forum/user_info.html', {
        'title': u.username,
        'user': u,
        'threads': u.threads.visible().select_related('topic')[:10],
        'replies': u.posts.visible().select_related('thread', 'user').order_by('-pub_date')[:30],
    })


class UserPosts(ListView):
    model = Post
    paginate_by = 15
    template_name = 'teacher_module/teacher_forum/user_replies.html'
    context_object_name = 'replies'

    def get_queryset(self):
        return Post.objects.visible().filter(
            user_id=self.kwargs.get('pk')
        ).select_related(
            'user', 'thread'
        ).prefetch_related(
            'user__forum_avatar'
        )

    def get_context_data(self, **kwargs):
        context = super(ListView, self).get_context_data(**kwargs)
        context['user'] = User.objects.get(pk=self.kwargs.get('pk'))
        context['panel_title'] = context['title'] = context['user'].username
        return context


class UserThreads(ListView):
    model = Post
    paginate_by = 15
    template_name = 'teacher_module/teacher_forum/user_threads.html'
    context_object_name = 'threads'

    def get_queryset(self):
        return Thread.objects.filter(
            user_id=self.kwargs.get('pk')
        ).select_related(
            'user', 'topic'
        ).prefetch_related(
            'user__forum_avatar'
        )

    def get_context_data(self, **kwargs):
        context = super(ListView, self).get_context_data(**kwargs)
        context['user'] = User.objects.get(pk=self.kwargs.get('pk'))
        context['panel_title'] = context['title'] = context['user'].username
        return context


class NotificationView(ListView):
    model = Notification
    paginate_by = 20
    template_name = 'teacher_module/teacher_forum/notifications.html'
    context_object_name = 'notifications'

    def get_queryset(self):
        Notification.objects.filter(to=self.request.user).update(read=True)
        return Notification.objects.filter(
            to=self.request.user
        ).select_related(
            'sender', 'thread', 'post'
        ).prefetch_related(
            'sender__forum_avatar', 'post__thread'
        ).order_by('-pub_date')

    def get_context_data(self, **kwargs):
        context = super(ListView, self).get_context_data(**kwargs)
        context['title'] = ("Notifications")
        return context


def edit_thread(request, pk):
    thread = Thread.objects.get(pk=pk)
    if thread.reply_count < 0:
        return HttpResponseForbidden(_('Editing is not allowed when thread has been replied'))
    if not thread.user == request.user:
        return HttpResponseForbidden(_('You are not allowed to edit other\'s thread'))
    if request.method == 'POST':
        form = ThreadEditForm(request.POST, instance=thread)
        if form.is_valid():
            t = form.save()
            return HttpResponseRedirect(reverse('forum:thread', kwargs={'pk': t.pk}))
    else:
        form = ThreadEditForm(instance=thread)

    return render(request, 'teacher_module/teacher_forum/edit_thread.html',
                  {'form': form, 'object': thread, 'title': ('Edit thread')})


@login_required
def edit_thread(request, pk):
    thread = Thread.objects.get(pk=pk)
    if thread.reply_count < 0:
        return HttpResponseForbidden(_('Editing is not allowed when thread has been replied'))
    if not thread.user == request.user:
        return HttpResponseForbidden(_('You are not allowed to edit other\'s thread'))
    if request.method == 'POST':
        form = ThreadEditForm(request.POST, instance=thread)
        if form.is_valid():
            t = form.save()
            return HttpResponseRedirect(reverse('teacher_thread', kwargs={'pk': t.pk}))
    else:
        form = ThreadEditForm(instance=thread)

    return render(request, 'teacher_module/teacher_forum/edit_thread.html',
                  {'form': form, 'object': thread, 'title': ('Edit thread')})


def CourseForum(request, course):
    course = CourseInfo.objects.get(pk=course)
    course_forum = None
    course_node_forum = None
    try:
        course_node_forum = NodeGroup.objects.get(title='Course')
    except ObjectDoesNotExist:
        NodeGroup.objects.create(title='Course', description='Root node for course Forum').save()
        course_node_forum = NodeGroup.objects.get(title='Course')

    try:
        course_forum = Topic.objects.get(course_associated_with=course)
    except ObjectDoesNotExist:
        Topic.objects.create(title=course.Course_Name, node_group=course_node_forum, course_associated_with=course,
                             center_associated_with=request.user.Center_Code, topic_icon="book").save()
        course_forum = Topic.objects.get(course_associated_with=course)

    return redirect('teacher_topic', pk=course_forum.pk)


def Topic_related_to_user(request, node_group=None):
    if node_group == None:
        own_center_general_topic = Topic.objects.filter(center_associated_with=request.user.Center_Code).filter(
            course_associated_with__isnull=True) | Topic.objects.filter(center_associated_with__isnull=True,
                                                                        course_associated_with__isnull=True)
        innings_Course_Code = InningGroup.objects.filter(Teacher_Code=request.user.id).values('Course_Code')
        assigned_topics = (
                Topic.objects.filter(course_associated_with__in=innings_Course_Code) | own_center_general_topic)

    else:
        own_center_general_topic = Topic.objects.filter(node_group=node_group.pk,
                                                        center_associated_with=request.user.Center_Code).filter(
            course_associated_with__isnull=True) | Topic.objects.filter(node_group=node_group.pk,
                                                                        center_associated_with__isnull=True,
                                                                        course_associated_with__isnull=True)
        innings_Course_Code = InningGroup.objects.filter(Teacher_Code=request.user.id).values('Course_Code')
        assigned_topics = (Topic.objects.filter(node_group=node_group.pk,
                                                course_associated_with__in=innings_Course_Code) | own_center_general_topic)
    return assigned_topics


def Thread_related_to_user(request):
    return Thread.objects.filter(topic__in=Topic_related_to_user(request))


from textblob import TextBlob


def get_top_thread_keywords(request, number_of_keyword):
    obj = Thread.objects.visible().filter(topic__in=Topic_related_to_user(request))
    word_counter = {}
    for eachx in obj:
        words = TextBlob(eachx.title).noun_phrases
        for eachword in words:
            for singleword in eachword.split(" "):
                if singleword in word_counter:
                    word_counter[singleword] += 1
                else:
                    word_counter[singleword] = 1

    popular_words = sorted(word_counter, key=word_counter.get, reverse=True)
    return popular_words[:number_of_keyword]


import operator
from django.db.models import Q
from functools import reduce


def ThreadSearchAjax(request, topic_id):
    threadkeywordList = request.GET.get('threadkeywordList').split("_")
    RelevantThread = []
    if topic_id:
        RelevantThread = Thread.objects.filter(topic=topic_id)
        pass
    else:
        RelevantTopics = Topic_related_to_user(request).values_list('pk')
        RelevantThread = Thread.objects.filter(topic__in=RelevantTopics)
        pass
    RelevantThread = RelevantThread.filter(reduce(operator.and_, (Q(title__contains=x) for x in threadkeywordList)))[:5]
    return render(request, 'teacher_module/teacher_forum/ThreadSearchAjax.html', {'RelevantThread': RelevantThread})


class SessionAdminInningInfoListView(ListView):
    model = InningInfo
    template_name = 'teacher_module/inninginfo_list.html'

    def get_queryset(self):
        return InningInfo.objects.filter(Center_Code=self.request.user.Center_Code, End_Date__gte=datetime.now(),
                                         inningmanager__memberinfoobj__pk=self.request.user.pk)


class SessionAdminInningInfoListViewInactive(ListView):
    model = InningInfo
    template_name = 'teacher_module/inninginfo_list_inactive.html'

    def get_queryset(self):
        return InningInfo.objects.filter(Center_Code=self.request.user.Center_Code, End_Date__lte=datetime.now(),
                                         inningmanager__memberinfoobj__pk=self.request.user.pk)


class SessionAdminInningInfoDetailView(InningInfoAuthMxnCls, DetailView):
    model = InningInfo
    template_name = 'teacher_module/inninginfo_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['SessionSurvey'] = SurveyInfo.objects.filter(Session_Code=self.kwargs['pk'])
        if InningManager.objects.filter(sessioninfoobj__pk=self.kwargs['pk']).exists():
            context['session_managers'] = get_object_or_404(InningManager, sessioninfoobj__pk=self.kwargs['pk'])
        return context


class GroupMappingUpdateView(UpdateView):
    model = GroupMapping
    form_class = GroupMappingForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['base_file'] = "teacher_module/base.html"
        return context

    def get_form_kwargs(self):
        kwargs = super(GroupMappingUpdateView, self).get_form_kwargs()
        kwargs.update({'request': self.request})
        return kwargs

    def form_valid(self, form):
        if form.is_valid():
            form.save()
            messages.add_message(self.request, messages.SUCCESS, 'Successfully updated.')
            return redirect('teachers_mysession_detail', form.initial['id'])


class InningGroupDetailView(InningGroupAuthMxnCls, DetailView):
    model = InningGroup
    template_name = 'teacher_module/inninggroup_detail.html'

    def form_valid(self, form):
        if form.is_valid():
            form.save()
            return redirect('teachers_mysession_list')


class InningGroupUpdateView(InningGroupAuthMxnCls, UpdateView):
    model = InningGroup
    form_class = InningGroupForm
    template_name = 'teacher_module/inning_group_update.html'

    def form_valid(self, form):
        messages.add_message(self.request, messages.SUCCESS, 'Course Teacher Allocation Updated.')
        self.object = form.save()
        return redirect('teachers_inninggroup_detail', self.kwargs.get('pk'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['base_file'] = "teacher_module/base.html"
        return context

    def get_form_kwargs(self):
        kwargs = super(InningGroupUpdateView, self).get_form_kwargs()
        kwargs.update({'request': self.request})
        return kwargs


class InningInfoUpdateView(UpdateView):
    model = InningInfo
    form_class = InningInfoForm
    template_name = 'teacher_module/changestudentgroup_form.html'

    def get_form_kwargs(self):
        kwargs = super(InningInfoUpdateView, self).get_form_kwargs()
        kwargs.update({'request': self.request})
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['datetime'] = datetime.now()
        context['base_file'] = 'teacher_module/base.html'
        return context

    def form_valid(self, form):
        if form.is_valid():
            form.save()
            messages.add_message(self.request, messages.SUCCESS, 'Successfully updated.')
            return redirect('teachers_mysession_detail', form.initial['id'])


class AttendanceListView(ListView):
    model = Attendance
    template_name = 'teacher_module/attendance/attendance_list.html'

    # def get_queryset(self):
    #     return Attendance.objects.filter(course=' #TODO make get_teacher_course function  in models.py')


class AttendanceCreateView(CreateView):
    model = Attendance
    form_class = AttendanceForm
    template_name = 'teacher_module/attendance/attendance_form.html'


class AttendanceDetailView(DetailView):
    model = Attendance
    template_name = 'teacher_module/attendance/attendance_detail.html'


class AttendanceUpdateView(UpdateView):
    model = Attendance
    form_class = AttendanceForm
    template_name = 'teacher_module/attendance/attendance_form.html'


from django.forms.models import modelformset_factory


def CourseAttendance(request, inningpk, course, attend_date):
    if InningInfoAuth(request, inningpk) != 1:  # if inning does not belong to the center of requested user.
        return redirect('login')
    global list_of_students
    studentattendancejson = []
    if not CourseInfo.objects.filter(pk=course).exists():
        messages.error(request,
                       "Course Does not exist.")
    # if datetime.strptime(attend_date, "%Y-%M-%d") > datetime.today().date():
    #     messages.error(request,
    #                        "You cannot take attendance of future date.")
    #     return HttpResponse('hello')

    if request.method == "POST":
        modelformset = AttendanceFormSetForm(request.POST or None, queryset=Attendance.objects.all())

        for cn, i in enumerate(modelformset.cleaned_data):
            if not isinstance(i['id'], int) and len(i) and i['id'] if len(i) else 0:
                a = Attendance.objects.get(pk=i['id'].pk)
                a.present = i['present']
                a.updated = datetime.utcnow()
                a.save()
            else:
                k = modelformset.forms[cn]
                k.save()
        pass
        messages.success(request, 'Submitted successfully')

    else:
        if InningInfo.objects.filter(pk=inningpk).exists():
            innings = InningInfo.objects.get(pk=inningpk)
            if MemberInfo.objects.filter(pk__in=innings.Groups.Students.all()).exists():
                list_of_students = MemberInfo.objects.filter(pk__in=innings.Groups.Students.all())

            AttendanceFormSetx = modelformset_factory(Attendance, form=AttendanceFormSetFormT,

                                                      extra=len(list_of_students))

            for x in list_of_students:
                a = Attendance.objects.filter(member_code__pk=x.pk, attendance_date=attend_date, course__pk=course)
                if a.exists():
                    print(a[0].pk)
                    studentattendancejson.append({
                        'attendance_date': a[0].attendance_date,
                        'present': a[0].present,
                        'member_code': a[0].member_code,
                        'course': a[0].course,
                        'id': a[0].pk,
                        'updated': a[0].updated,
                    })
                else:
                    studentattendancejson.append({
                        'attendance_date': attend_date,
                        'present': False,
                        'member_code': x,
                        'course': course,
                    })
            formset = AttendanceFormSetx(queryset=Attendance.objects.none(),
                                         initial=studentattendancejson)
            context = {
                'attendance': formset,
                'course': CourseInfo.objects.get(pk=course),
                'inning': InningInfo.objects.get(pk=inningpk),
                'attend_date': attend_date,
            }
            return render(request, 'teacher_module/attendance/course_attendance_form.html', context)

        else:
            messages.error(request,
                           "Inning does not exist.")
    return redirect('course_attendance_list', inningpk, course, attend_date)


def CourseAttendanceList(request, inningpk=None, course=None, attend_date=None):
    if inningpk:
        if InningInfoAuth(request, inningpk) != 1:  # if inning does not belong to the center of requested user.
            return redirect('login')
    formset = None
    session_list = []
    session_course = []
    if attend_date == None:
        attend_date = str(datetime.today().date())
    studentattendancejson = []
    if InningInfo.objects.filter(pk=inningpk).exists():
        innings = InningInfo.objects.get(pk=inningpk)
        if MemberInfo.objects.filter(pk__in=innings.Groups.Students.all()).exists():
            list_of_students = MemberInfo.objects.filter(pk__in=innings.Groups.Students.all())

        AttendanceFormSetx = modelformset_factory(Attendance,
                                                  fields=['present', 'member_code', 'course', 'attendance_date', 'id'],
                                                  extra=len(list_of_students))

        for x in list_of_students:
            a = Attendance.objects.filter(member_code__pk=x.pk, attendance_date=attend_date, course__pk=course)
            if a.exists():
                studentattendancejson.append({
                    'attendance_date': a[0].attendance_date,
                    'present': a[0].present,
                    'member_code': a[0].member_code,
                    'course': a[0].course,
                    'id': a[0].pk,
                    'updated': a[0].updated,

                })
            else:
                studentattendancejson.append({
                    'attendance_date': attend_date,
                    'present': False,
                    'member_code': x,
                    'course': course,
                    'updated': None
                })
        formset = AttendanceFormSetx(queryset=Attendance.objects.none(),
                                     initial=studentattendancejson)

    # session_list = InningInfo.objects.filter(Course_Group__in = a)
    ig = InningGroup.objects.filter(Teacher_Code=request.user)
    # session_list = InningInfo.objects.filter(Course_Group__in = ig)

    if not inningpk and course:
        c = CourseInfo.objects.get(pk=course)
        if c:
            inning_info = InningInfo.objects.filter(Course_Group__Teacher_Code__pk=request.user.pk,
                                                    Course_Group__Course_Code__pk=c.pk, Use_Flag=True,
                                                    End_Date__gt=datetime_now).distinct()
            session_list.append(inning_info)

    else:
        for i in ig:
            inning_info = InningInfo.objects.filter(Course_Group__Teacher_Code__pk=request.user.pk,
                                                    Course_Group__pk=i.pk, Use_Flag=True,
                                                    End_Date__gt=datetime_now).distinct()
            if inning_info.exists():
                session_course.append([
                    {
                        'course': i.Course_Code,
                        'session': inning_info,
                    },
                ])
                # for i in inning_info:
                #     if len(session_list) > 0:
                #         for m in session_list:
                #             for n in m:
                #                 if not i.pk == n.pk:
                #                     session_list.append(inning_info)
                #     else:
                #         session_list.append(inning_info)
        for i in session_course:
            for m in i:
                session_list += (list(m['session'].values_list('pk', flat=True)))
        session_list = [InningInfo.objects.filter(pk__in=set(session_list))]
    context = {
        'attendance': formset,
        'course': CourseInfo.objects.get(pk=course) if course else None,
        'inning': InningInfo.objects.get(pk=inningpk) if inningpk else None,
        'attend_date': attend_date,
        'session_list': session_list,
        'session_course': session_course,
        'todays_date': datetime_now,
    }

    return render(request, 'attendance/course_attendance_list.html', context)


# chapter progress of students function
def maintainLastPageofStudent(courseid, chapterid, studentid, currentPageNumber=None, totalPage=None, createFile=True):
    path = os.path.join(settings.MEDIA_ROOT, ".chapterProgressData", courseid, chapterid)
    try:
        os.makedirs(path)
    except Exception as e:
        pass
    student_data_file = os.path.join(path, studentid + '.txt')
    if os.path.isfile(student_data_file):
        student_file = open(student_data_file, "r")
        if student_file.mode == 'r':
            x = student_file.read()
            x = x.split(',')
            LastPageNumberFromFileSystem, totalPage = x[0], x[1]
            student_file.close()
        if currentPageNumber is None:
            return LastPageNumberFromFileSystem, totalPage
        if int(currentPageNumber) > int(LastPageNumberFromFileSystem):
            student_file = open(student_data_file, "w+")
            if currentPageNumber and totalPage:
                student_file.write(currentPageNumber + "," + totalPage)
                student_file.close()
        else:
            student_file = open(student_data_file, "r")
            if student_file.mode == 'r':
                x = student_file.read()
                x = x.split(',')
                LastPageNumberFromFileSystem, totalPage = x[0], x[1]
                student_file.close()
    else:
        if createFile:
            student_file = open(student_data_file, "w+")
            if currentPageNumber and totalPage:
                student_file.write(currentPageNumber + "," + totalPage)
            else:
                student_file.write("0,0")

            student_file.close()
        else:
            return None, None
    return currentPageNumber, totalPage


def chapterStudentProgress(request, course, pk, inningpk=None):
    session_list = []
    studentjson = []

    course = get_object_or_404(CourseInfo, pk=course)
    chapter = get_object_or_404(ChapterInfo, pk=pk)

    if course and chapter:
        inning_info = InningInfo.objects.filter(Course_Group__Teacher_Code__pk=request.user.pk,
                                                Course_Group__Course_Code__pk=course.pk, Use_Flag=True,
                                                End_Date__gt=datetime_now).distinct()
        session_list.append(inning_info)

        if inning_info.count() > 0:
            if inningpk:
                if inning_info.filter(pk=inningpk).exists():
                    innings = inning_info.get(pk=inningpk)
                else:
                    innings = inning_info.all().first()
            else:
                innings = inning_info.all().first()

            if MemberInfo.objects.filter(pk__in=innings.Groups.Students.all()).exists():
                list_of_students = MemberInfo.objects.filter(pk__in=innings.Groups.Students.all())

            for x in list_of_students:
                currentPage, totalpage = maintainLastPageofStudent(str(course.pk), str(chapter.pk), str(x.id),
                                                                   createFile=False)
                if totalpage is not None and int(totalpage) > 0 and int(currentPage) > 0:
                    progresspercent = int(currentPage) * 100 / int(totalpage)
                else:
                    progresspercent = 1
                studentjson.append({
                    'member_code': x,
                    'currentpage': currentPage,
                    'totalpage': totalpage,
                    'progresspercent': progresspercent,
                })

    context = {
        'course': course,
        'chapter': chapter,
        'inning': InningInfo.objects.get(pk=inningpk) if inningpk else None,
        'session_list': session_list,
        'studentjson': studentjson,
    }

    return render(request, 'teacher_module/chapterProgress.html', context)


def teacherAttendance(request, courseid, createFile=True):
    chapters = []
    pagenumber = []
    if request.GET.get('chapterid'):
        chapterid = request.GET.get('chapterid')
        pagenumber = request.GET.get('pagenumber')
    today = datetime_now.strftime("%m%d%Y")
    path = os.path.join(settings.MEDIA_ROOT, ".teacherAttendanceData", str(courseid), today)
    try:
        os.makedirs(path)
    except Exception as e:
        pass
    teacher_data_file = os.path.join(path, str(request.user.pk) + '.txt')

    if os.path.isfile(teacher_data_file):
        new_data = None
        with open(teacher_data_file) as json_file:
            data = json.load(json_file)
            start_time = data['start_time']
            # end_time = data['end_time']
            numberoftimesopened = int(data['numberoftimesopened'])
            new_data = data

        if createFile:
            numberoftimesopened += 1
            new_data.update({
                'end_time': datetime_now.strftime("%m/%d/%Y, %H:%M:%S"),
                'numberoftimesopened': numberoftimesopened,
            })
            if request.GET.get('chapterid'):
                chapters = new_data['chapters']
                create = 0
                for x in new_data['chapters']:
                    if request.GET.get('chapterid') == x['chapterid']:
                        create = 1
                        if request.GET.get('pagenumber') not in x['pagenumber']:
                            x['pagenumber'].append(request.GET.get('pagenumber'))
                            break
                if create == 0:
                    new_data['chapters'] = new_data['chapters'] + [{
                        'chapterid': request.GET.get('chapterid'),
                        'pagenumber': [request.GET.get('pagenumber'), ]
                    }]
            with open(teacher_data_file, 'w+') as teacher_data_file:
                json.dump(new_data, teacher_data_file, indent=4)
    else:
        if createFile:
            data = {
                'start_time': datetime_now.strftime("%m/%d/%Y, %H:%M:%S"),
                'end_time': datetime_now.strftime("%m/%d/%Y, %H:%M:%S"),
                'numberoftimesopened': 1,
            }
            if request.GET.get('chapterid'):
                chapters.append({
                    'chapterid': request.GET.get('chapterid'),
                    'pagenumber': [request.GET.get('pagenumber'), ]
                })
                data.update({
                    'chapters': chapters,
                })
            with open(teacher_data_file, 'w+') as teacher_file:
                json.dump(data, teacher_file, indent=4)

    return HttpResponse('success')


def Meet(request, ):
    meetcode = request.user.id
    for i in request.user.password[-5:]:
        meetcode *= ord(i)
    print(meetcode)
    return render(request, 'teacher_module/meet.html', {"meetcode": meetcode})


def QuizMarkingCSV(request, quiz_pk):
    quiz = Quiz.objects.get(pk=int(quiz_pk))
    quiz_sittings = Sitting.objects.filter(quiz=quiz, complete=True)
    total_score = quiz.get_max_score

    mcquestions = quiz.mcquestion.all()
    tfquestions = quiz.tfquestion.all()
    saquestions = quiz.saquestion.all()
    extra_row_1 = {'S.N.': 'Full Score', 'Student Username': '', 'Start Datetime': '', 'End Datetime': '',
                   'Percentage': ''}
    extra_row_2 = {'S.N.': 'Correct Answer', 'Student Username': '', 'Start Datetime': '', 'End Datetime': '',
                   'Percentage': ''}

    # Deining column names
    column_names = ['S.N.', 'Student Username', 'Start Datetime', 'End Datetime']
    answer_name = "O/X"
    mcq_full_score, tfq_full_score, saq_full_score = 0, 0, 0
    color_column = []
    for i, mcquestion in enumerate(mcquestions):
        question_name = "MCQ" + str(i + 1)
        column_names.append(question_name)
        column_names.append(answer_name + " M" + str(i + 1))
        color_column.append(answer_name + " M" + str(i + 1))
        mcq_full_score += mcquestion.score
        extra_row_1[question_name] = mcquestion.score
        extra_row_2[question_name] = mcquestion.get_correct_answer()
    for i, tfquestion in enumerate(tfquestions):
        question_name = "TFQ" + str(i + 1)
        column_names.append(question_name)
        column_names.append(answer_name + " T" + str(i + 1))
        color_column.append(answer_name + " T" + str(i + 1))
        tfq_full_score += tfquestion.score
        extra_row_1[question_name] = tfquestion.score
        extra_row_2[question_name] = tfquestion.correct
    for i, saquestion in enumerate(saquestions):
        question_name = "SAQ" + str(i + 1)
        column_names.append(question_name)
        column_names.append(answer_name + " S" + str(i + 1))
        saq_full_score += saquestion.score
        extra_row_1[question_name] = saquestion.score
    column_names.extend(["MCQ Score", "TFQ Score", "SAQ Score", "Total Score", "Percentage"])

    df = pd.DataFrame(columns=column_names)

    extra_row_1["MCQ Score"] = mcq_full_score
    extra_row_1["TFQ Score"] = tfq_full_score
    extra_row_1["SAQ Score"] = saq_full_score
    extra_row_1["Total Score"] = total_score
    df = df.append(extra_row_1, ignore_index=True)
    df = df.append(extra_row_2, ignore_index=True)
    counter = 0

    for quiz_sitting in quiz_sittings:
        start_date = ''
        end_date = ''
        counter += 1
        if quiz_sitting.start:
            start_date = quiz_sitting.start.replace(tzinfo=None)
        if quiz_sitting.end:
            end_date = quiz_sitting.end.replace(tzinfo=None)
        new_row = {'S.N.': counter, 'Student Username': quiz_sitting.user, 'Start Datetime': start_date,
                   'End Datetime': end_date,
                   'Total Score': quiz_sitting.get_score_correct, 'Percentage': quiz_sitting.get_percent_correct}

        user_answers = json.loads(quiz_sitting.user_answers)
        totalmcq_score = 0.0
        totaltfq_score = 0.0
        totalsaq_score = 0.0

        for i, mcquestion in enumerate(mcquestions):
            question_name = "MCQ" + str(i + 1)
            question_name_value = user_answers.get(str(mcquestion.id))
            if question_name_value:
                ans_value = Answer.objects.get(id=int(question_name_value)).content
            else:
                ans_value = ''
            new_row[question_name] = ans_value
            if mcquestion.check_if_correct(question_name_value):
                new_row[answer_name + " M" + str(i + 1)] = "✔"
                totalmcq_score += mcquestion.score
            else:
                new_row[answer_name + " M" + str(i + 1)] = "❌"
        for i, tfquestion in enumerate(tfquestions):
            question_name = "TFQ" + str(i + 1)
            question_name_value = user_answers.get(str(tfquestion.id))
            new_row[question_name] = question_name_value
            if tfquestion.check_if_correct(question_name_value):
                new_row[answer_name + " T" + str(i + 1)] = "✔"
                totaltfq_score += tfquestion.score
            else:
                new_row[answer_name + " T" + str(i + 1)] = "❌"
        for i, saquestion in enumerate(saquestions):
            question_name = "SAQ" + str(i + 1)
            question_name_value = user_answers.get(str(saquestion.id))
            new_row[question_name] = question_name_value

            user_ans = str(quiz_sitting.user_answers)
            saq_id = '"' + str(saquestion.id) + '":'
            end_index = user_ans.find(saq_id)
            score_index = user_ans.count('": "', 0, end_index)
            score_list = str(quiz_sitting.score_list).split(',')
            new_row[answer_name + " S" + str(i + 1)] = score_list[score_index]
            if str(score_list[score_index]) and str(score_list[score_index]) != 'not_graded':
                totalsaq_score += float(score_list[score_index])

        new_row['MCQ Score'] = totalmcq_score
        new_row['TFQ Score'] = totaltfq_score
        new_row['SAQ Score'] = totalsaq_score
        # append row to the dataframe
        df = df.append(new_row, ignore_index=True)

    df = df.set_index('S.N.', drop=True)

    def color_negative_red(val):
        color = 'white'
        if val == '✔':
            color = '#00b0f0'
        if val == '❌':
            color = 'red'
        return 'background-color: %s' % color

    df = df.style.applymap(color_negative_red, subset=color_column)
    # print(df)
    # return HttpResponse("<h4>Student All Course Progress download</h4>")
    with BytesIO() as b:
        # Use the StringIO object as the filehandle.
        writer = pd.ExcelWriter(b, engine='xlsxwriter')
        # df.index += 1
        df.index.name = 'S.N.'
        sheet_name = str(quiz.title)
        sheet_name = re.sub('[^A-Za-z0-9_ .]+', '', sheet_name)  # remove special characters
        if len(sheet_name) > 28:
            sheet_name = sheet_name[:27] + ' ..'
        # df.to_excel(writer, sheet_name=sheet_name)

        df.to_excel(writer, sheet_name=sheet_name, startrow=1, header=False)

        # Get the xlsxwriter workbook and worksheet objects.
        workbook = writer.book
        worksheet = writer.sheets[sheet_name]

        # Add a header format.
        header_format = workbook.add_format({
            'bold': True,
            'text_wrap': True,
            'valign': 'center',
            'fg_color': 'yellow',
            'border': 1})

        # Write the column headers with the defined format.
        for col_num, value in enumerate(df.columns.values):
            worksheet.write(0, col_num + 1, value, header_format)

        # Close the Pandas Excel writer and output the Excel file.
        writer.save()
        response = HttpResponse(b.getvalue(),
                                content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;charset=UTF-8')
        response['Content-Disposition'] = 'attachment; filename="' + 'QuizMarking_' + sheet_name + '.xlsx"'
        return response
