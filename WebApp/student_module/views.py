import uuid
from datetime import datetime

from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.views import PasswordContextMixin
from django.core.exceptions import ObjectDoesNotExist
from django.core.files.storage import FileSystemStorage
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponseRedirect, HttpResponseForbidden, HttpResponse
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.utils.translation import gettext as _
from django.views import View
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters
from django.views.generic import ListView, DetailView, TemplateView
from django.views.generic.edit import FormView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from textblob import TextBlob

from LMS import settings
from WebApp.filters import MyCourseFilter
from WebApp.forms import UserUpdateForm
from WebApp.models import CourseInfo, GroupMapping, InningInfo, ChapterInfo, AssignmentInfo, MemberInfo, \
    AssignmentQuestionInfo, AssignAnswerInfo, InningGroup
from forum.forms import ThreadForm, TopicForm, ReplyForm, ThreadEditForm
from forum.models import NodeGroup, Thread, Topic, Post, Notification
from quiz.models import Quiz
from survey.models import SurveyInfo, CategoryInfo, OptionInfo, SubmitSurvey, AnswerInfo, QuestionInfo
from .misc import get_query
from ..views import chapterProgressRecord, getCourseProgress

datetime_now = datetime.now()

User = get_user_model()

from quiz.views import QuizUserProgressView, Sitting, Progress


def start(request):
    global courses, activeassignments, sessions, batches
    if request.user.Is_Student:
        batches = GroupMapping.objects.filter(Students__id=request.user.id, Center_Code=request.user.Center_Code)
        sessions = []
        if batches:
            for batch in batches:
                # Filtering out only active sessions
                session = InningInfo.objects.filter(Groups__id=batch.id, End_Date__gt=datetime_now)
                sessions += session
        courses = set()
        activeassignments = []
        if sessions:
            for session in sessions:
                course = session.Course_Group.filter(Course_Code__Use_Flag=True)
                courses.update(course)
            for course in courses:
                activeassignments += AssignmentInfo.objects.filter(
                    Assignment_Deadline__gte=datetime_now, Course_Code=course.Course_Code.id,
                    Chapter_Code__Use_Flag=True)[:7]
    sittings = Sitting.objects.filter(user=request.user)
    wordCloud = Thread.objects.filter(user__Center_Code=request.user.Center_Code)
    thread_keywords = get_top_thread_keywords(request, 10)

    return render(request, 'student_module/dashboard.html',
                  {'GroupName': batches, 'Group': sessions, 'Course': courses,
                   'activeAssignments': activeassignments, 'sittings': sittings, 'wordCloud': wordCloud,
                   'get_top_thread_keywords': thread_keywords})


class PasswordChangeView(PasswordContextMixin, FormView):
    form_class = PasswordChangeForm
    success_url = reverse_lazy('student_user_profile')
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


def student_editprofile(request):
    if not request.user.is_authenticated:
        return HttpResponse("you are not authenticated", {'error_message': 'Error Message Customize here'})
    post = get_object_or_404(MemberInfo, pk=request.user.id)
    if request.method == "POST":

        form = UserUpdateForm(request.POST, request.FILES, instance=post)

        if form.is_valid():
            post.date_last_update = datetime.now()
            post.save()
            return redirect('student_user_profile')
    else:

        form = UserUpdateForm(request.POST, request.FILES, instance=post)

    return render(request, 'student_module/editprofile.html', {'form': form})


def quiz(request):
    return render(request, 'student_module/quiz.html')


def quizzes(request):
    return render(request, 'student_module/quizzes.html')


def calendar(request):
    if request.user.Is_Student:
        batches = GroupMapping.objects.filter(Students__id=request.user.id, Center_Code=request.user.Center_Code)
        sessions = []
        if batches:
            for batch in batches:
                # Filtering out only active sessions
                session = InningInfo.objects.filter(Groups__id=batch.id, End_Date__gt=datetime_now)
                sessions += session
        courses = set()
        activeassignments = []
        if sessions:
            for session in sessions:
                course = session.Course_Group.all()
                courses.update(course)
            for course in courses:
                activeassignments += AssignmentInfo.objects.filter(
                    Course_Code=course.Course_Code.id, Chapter_Code__Use_Flag=True)[:7]

        student_group = request.user.groupmapping_set.all()
        student_session = InningInfo.objects.filter(Groups__in=student_group)
        active_student_session = InningInfo.objects.filter(Groups__in=student_group, End_Date__gt=datetime_now)
        student_course = InningGroup.objects.filter(inninginfo__in=active_student_session).values("Course_Code")

        # Predefined category name "general, session, course, system"
        general_survey = SurveyInfo.objects.filter(Category_Code__Category_Name__iexact="general",
                                                   Center_Code=request.user.Center_Code, Use_Flag=True)
        session_survey = SurveyInfo.objects.filter(Category_Code__Category_Name__iexact="session",
                                                   Session_Code__in=student_session, Use_Flag=True)
        course_survey = SurveyInfo.objects.filter(Category_Code__Category_Name__iexact="course",
                                                  Course_Code__in=student_course, Use_Flag=True)
        system_survey = SurveyInfo.objects.filter(Center_Code=None, Use_Flag=True)

        my_queryset = None
        my_queryset = general_survey | session_survey | course_survey | system_survey
        my_queryset = my_queryset.filter(End_Date__gt=timezone.now(), Survey_Live=False)

        return render(request, 'student_module/calendar.html',
                      {'activeassignments': activeassignments, 'activesurvey': my_queryset})


class MyCoursesListView(ListView):
    model = CourseInfo
    template_name = 'student_module/myCourse.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        batches = GroupMapping.objects.filter(Students__id=self.request.user.id,
                                              Center_Code=self.request.user.Center_Code)
        sessions = []
        if batches:
            for batch in batches:
                # Filtering out only active sessions
                session = InningInfo.objects.filter(Groups__id=batch.id, End_Date__gt=datetime_now)
                sessions += session
        courses = InningGroup.objects.none()
        if sessions:
            for session in sessions:
                course = session.Course_Group.filter(Course_Code__Use_Flag=True)
                courses |= course

        courses = courses.distinct()
        filtered_qs = MyCourseFilter(self.request.GET, queryset=courses).qs
        filtered_qs = filtered_qs.filter(Course_Code__in=context['object_list'].values_list('pk'))
        paginator = Paginator(filtered_qs, 8)
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
        qset = self.model.objects.all()
        queryset = self.request.GET.get('studentmycoursequery')
        if queryset:
            queryset = queryset.strip()
            qset = qset.filter(Course_Name__icontains=queryset)
            if not len(qset):
                messages.error(
                    self.request, 'Sorry no courses found! Try with a different keyword')
        # you don't need this if you set up your ordering on the model
        qset = qset.order_by("-id")
        return qset


class MyAssignmentsListView(ListView):
    model = AssignmentInfo
    template_name = 'student_module/myassignments_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['Assignment'], context['activeAssignment'], context['expiredAssignment'] = [], [], []
        Assignment, activeAssignment, expiredAssignment = [], [], []
        Sessions = []
        Courses = set()

        context['currentDate'] = datetime.now()
        GroupName = GroupMapping.objects.filter(Students__id=self.request.user.id)
        for group in GroupName:
            Sessions += InningInfo.objects.filter(Groups__id=group.id)

        for session in Sessions:
            for coursegroup in session.Course_Group.filter(Course_Code__Use_Flag=True):
                Courses.add(coursegroup.Course_Code)

        for course in Courses:
            Assignment.append(AssignmentInfo.objects.filter(
                Course_Code__id=course.id, Use_Flag=True, Chapter_Code__Use_Flag=True))
            activeAssignment.append(AssignmentInfo.objects.filter(
                Course_Code__id=course.id, Assignment_Deadline__gte=datetime_now, Use_Flag=True,
                Chapter_Code__Use_Flag=True))
            expiredAssignment.append(AssignmentInfo.objects.filter(
                Course_Code__id=course.id, Assignment_Deadline__lte=datetime_now, Use_Flag=True,
                Chapter_Code__Use_Flag=True))
        context['Assignment'].append(Assignment)
        context['activeAssignment'].append(activeAssignment)
        context['expiredAssignment'].append(expiredAssignment)
        return context


class CourseInfoListView(ListView):
    model = CourseInfo
    template_name = 'student_module/courseinfo_list.html'

    paginate_by = 6

    def get_queryset(self):
        qs = self.model.objects.all()

        query = self.request.GET.get('coursequery')
        if query:
            query = query.strip()
            qs = qs.filter(Course_Name__icontains=query)
            if not len(qs):
                messages.error(
                    self.request, 'Sorry no course found! Try with a different keyword')
        # you don't need this if you set up your ordering on the model
        qs = qs.order_by("-id")
        return qs


class CourseInfoDetailView(DetailView):
    model = CourseInfo
    template_name = 'student_module/courseinfo_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['chapters'] = ChapterInfo.objects.filter(
            Course_Code=self.kwargs.get('pk'), Use_Flag=True).order_by('Chapter_No')
        context['surveycount'] = SurveyInfo.objects.filter(
            Course_Code=self.kwargs.get('pk'))
        context['quizcount'] = Quiz.objects.filter(
            course_code=self.kwargs.get('pk'), draft=False, exam_paper=True, chapter_code=None)
        context['numberOfQuizExclExams'] = Quiz.objects.filter(
            chapter_code__in=context['chapters'].values_list('pk'),
            exam_paper=False,
            draft=False)
        context['topic'] = Topic.objects.filter(
            course_associated_with=self.kwargs.get('pk'))

        context['student_data'] = getCourseProgress(self.object, [self.request.user], context['chapters'])
        return context


class ChapterInfoListView(ListView):
    model = ChapterInfo


class ChapterInfoDetailView(DetailView):
    model = ChapterInfo
    template_name = 'student_module/chapterinfo_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['assignments'] = AssignmentInfo.objects.filter(
            Chapter_Code=self.kwargs.get('pk'), Use_Flag=True)
        context['post_quizes'] = Quiz.objects.filter(
            chapter_code=self.kwargs.get('pk'), draft=False, post_test=True)
        context['pre_quizes'] = Quiz.objects.filter(
            chapter_code=self.kwargs.get('pk'), draft=False, pre_test=True)

        return context


class AssignmentInfoDetailView(DetailView):
    model = AssignmentInfo
    template_name = 'student_module/assignmentinfo_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['Questions'] = AssignmentQuestionInfo.objects.filter(
            Assignment_Code=self.kwargs.get('pk'))
        context['Course_Code'] = get_object_or_404(
            CourseInfo, pk=self.kwargs.get('course'))
        context['Chapter_No'] = get_object_or_404(
            ChapterInfo, pk=self.kwargs.get('chapter'))
        context['Answers'] = []
        AnsweredQuestion = set()
        Question = set()

        for question in context['Questions']:
            Answer = AssignAnswerInfo.objects.filter(
                Student_Code=self.request.user.pk, Question_Code=question.id)
            context['Answers'] += Answer
            Question.add(question.id)
        # print (context['Answers'])
        for answers in context['Answers']:
            # print (answers.Question_Code.id)
            AnsweredQuestion.add(answers.Question_Code.id)
        # print(Question)
        # print(context['AnsweredQuestion'])
        context['notAnswered'] = Question - AnsweredQuestion
        # context['Assignment_Code'] = get_object_or_404(AssignmentInfo, pk=self.kwargs.get('assignment'))
        return context


class submitAnswer(View):
    model = AssignAnswerInfo()

    def post(self, request, *args, **kwargs):
        if request.GET.get('editanswer'):
            Obj = AssignAnswerInfo.objects.get(pk=int(request.GET.get('editanswer')))
        else:
            Obj = AssignAnswerInfo()
        Obj.Assignment_Answer = request.POST["Assignment_Answer"]
        Obj.Student_Code = MemberInfo.objects.get(
            pk=request.POST["Student_Code"])
        Obj.Question_Code = AssignmentQuestionInfo.objects.get(
            pk=request.POST["Question_Code"])
        Assignment_Code = Obj.Question_Code.Assignment_Code
        if bool(request.FILES.get('Assignment_File', False)) == True:
            media = request.FILES['Assignment_File']
            # print(media)
            if media.size / 1024 > 10240:
                return JsonResponse(data={'status': 'Fail', "msg": "File size exceeds 10MB"}, status=500)
            path = settings.MEDIA_ROOT
            name = (str(uuid.uuid4())).replace('-', '') + '.' + media.name.split('.')[-1]
            fs = FileSystemStorage(location=path + '/assignments/' + str(Assignment_Code.id))
            filename = fs.save(name, media)
            Obj.Question_Media_File = 'assignments/' + str(Assignment_Code.id) + name
            Obj.Assignment_File = media
        Obj.save()

        return JsonResponse(
            data={'Message': 'Success'}
        )


def ProfileView(request):
    return render(request, 'student_module/profile.html')


# def questions_student(request):
#     return render(request, 'student_module/questions_student.html')

class questions_student(ListView):
    model = SurveyInfo
    template_name = 'student_module/questions_student.html'

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


class questions_student_detail(DetailView):
    model = SurveyInfo
    template_name = 'student_module/questions_student_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['questions'] = QuestionInfo.objects.filter(
            Survey_Code=self.kwargs.get('pk')).order_by('pk')
        context['options'] = OptionInfo.objects.filter(
            Question_Code__in=QuestionInfo.objects.filter(Survey_Code=self.object.id)
        )
        context['saq_answers'] = AnswerInfo.objects.filter(
            Question_Code__in=QuestionInfo.objects.filter(Survey_Code=self.object.id, Question_Type='SAQ')
        )
        try:
            context['submit_survey'] = SubmitSurvey.objects.get(
                Survey_Code__id=self.object.id,
                Student_Code__id=self.request.user.id
            )
        except SubmitSurvey.DoesNotExist:
            context['submit_survey'] = None

        if context['submit_survey']:
            for x in context['options']:
                if len(context['submit_survey'].answerinfo.filter(Answer_Value=x.id)) > 0:
                    x.was_chosen = True
                else:
                    x.was_chosen = False

            for x in context['questions']:
                try:
                    x.answer = AnswerInfo.objects.get(
                        Submit_Code=context['submit_survey'].id, Question_Code=x.id)
                except AnswerInfo.DoesNotExist:
                    x.answer = None

            context['can_submit'] = False


        else:
            if self.object.End_Date > datetime.now(timezone.utc):
                context['can_submit'] = True
            else:
                context['can_submit'] = False
                context['datetimeexpired'] = 1
        return context


class questions_student_detail_history(DetailView):
    model = SurveyInfo
    template_name = 'student_module/questions_student_detail_history.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['questions'] = QuestionInfo.objects.filter(
            Survey_Code=self.kwargs.get('pk')).order_by('pk')

        context['options'] = OptionInfo.objects.all()
        context['submit'] = SubmitSurvey.objects.all()

        return context


class ParticipateSurvey(View):

    def post(self, request, *args, **kwargs):
        surveyId = request.POST["surveyInfoId"]
        userId = self.request.user.id
        print(len(SubmitSurvey.objects.filter(Survey_Code__id=surveyId, Student_Code__id=userId)))
        if len(SubmitSurvey.objects.filter(Survey_Code__id=surveyId, Student_Code__id=userId)) > 0:
            messages.add_message(request, messages.ERROR,
                                 'You have already submitted and can not participate multiple times')
            return redirect('questions_student')

        submitSurvey = SubmitSurvey()
        submitSurvey.Survey_Code = SurveyInfo.objects.get(id=surveyId)
        submitSurvey.Student_Code = MemberInfo.objects.get(id=userId)
        submitSurvey.save()

        for question in QuestionInfo.objects.filter(Survey_Code=surveyId):
            optionId = request.POST.get(str(question.id), None)
            answerObject = AnswerInfo()
            answerObject.Answer_Value = optionId
            answerObject.Question_Code = question
            answerObject.Submit_Code = submitSurvey
            answerObject.save()
        messages.add_message(request, messages.SUCCESS, 'Your Survey has been submitted successfully.')
        if 'iframe' in request.GET:
            return redirect(reverse('questions_student') + '?iframe=' + self.request.GET.get(
                'iframe'))
        else:
            return redirect('questions_student')


class surveyFilterCategory_student(ListView):
    model = SurveyInfo
    template_name = 'student_module/questions_student_listView.html'
    # template_name = 'survey/common/surveyinfo_expireView.html'

    paginate_by = 6

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.GET = None

    def get_queryset(self):
        # try:
        category_name = self.request.GET['category_name'].lower()
        date_filter = self.request.GET['date_filter'].lower()
        # student related data
        student_group = self.request.user.groupmapping_set.all()
        student_session = InningInfo.objects.filter(Groups__in=student_group)
        active_student_session = InningInfo.objects.filter(Groups__in=student_group, End_Date__gt=datetime_now)
        student_course = InningGroup.objects.filter(inninginfo__in=active_student_session).values("Course_Code")

        # Predefined category name "general, session, course, system"
        general_survey = SurveyInfo.objects.filter(Category_Code__Category_Name__iexact="general",
                                                   Center_Code=self.request.user.Center_Code, Use_Flag=True)
        session_survey = SurveyInfo.objects.filter(Category_Code__Category_Name__iexact="session",
                                                   Session_Code__in=student_session, Use_Flag=True)
        course_survey = SurveyInfo.objects.filter(Category_Code__Category_Name__iexact="course",
                                                  Course_Code__in=student_course, Use_Flag=True)
        system_survey = SurveyInfo.objects.filter(Center_Code=None, Use_Flag=True)

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
    # print("Error occured")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['currentDate'] = datetime.now()
        context['category_name'] = self.request.GET['category_name'].lower()
        context['date_filter'] = self.request.GET['date_filter'].lower()

        submitSurveyQuerySet = SubmitSurvey.objects.filter(
            Student_Code=self.request.user.id)
        context['submittedSurvey'] = [
            el.Survey_Code.id for el in submitSurveyQuerySet]

        return context


# <===============================Forum==================================================>
class Index(ListView):
    model = Thread
    template_name = 'student_module/student_forum/forumIndex.html'
    context_object_name = 'threads'

    # def get_queryset(self):
    #     nodegroups = NodeGroup.objects.all()
    #     threadqueryset = Thread.objects.none()
    #     for ng in nodegroups:
    #         topics = Topic.objects.filter(node_group=ng.pk).filter(id__in=Topic_related_to_user(self.request))
    #         for topic in topics:
    #             threads = Thread.objects.visible().filter(topic=topic.pk).order_by('pub_date').filter(
    #                 topic_id__in=Topic_related_to_user(self.request))[:4]
    #             print("threads", threads)
    #             threadqueryset |= threads
    #     return threadqueryset

    def get_context_data(self, **kwargs):
        context = super(ListView, self).get_context_data(**kwargs)
        nodegroups = NodeGroup.objects.all()
        threads = []

        # innings = InningInfo.objects.filter(Groups__in=GroupMapping.objects.filter(Students__pk=self.request.user.pk))
        # own_courses_forum_topics = Topic.objects.none()
        for ng in nodegroups:
            thread_counter = 0
            # general_topics = Topic.objects.filter(node_group=ng.pk, center_associated_with= self.request.user.Center_Code, course_associated_with__isnull=True) | Topic.objects.filter(node_group=ng.pk, center_associated_with__isnull= True, course_associated_with__isnull=True)
            # if innings:
            #     courses = InningGroup.objects.filter(inninginfo__in=innings).values_list('Course_Code__pk')
            #     own_courses_forum_topics = Topic.objects.filter(node_group=ng.pk, course_associated_with__in=courses)
            # topics = general_topics | own_courses_forum_topics

            topics = Topic_related_to_user(self.request, node_group=ng)
            for topic in topics:
                thread_counter += topic.visible_threads_count
            if thread_counter == 0:
                nodegroups = nodegroups.exclude(pk=ng.pk)
            else:

                thread = Thread.objects.visible().filter(topic_id__in=topics).order_by('pub_date')[:4]
                threads += thread

        context['nodegroups'] = nodegroups
        context['threads'] = threads
        context['panel_title'] = _('New Threads')
        context['title'] = _('Index')
        context['topics'] = Topic.objects.all().filter(id__in=Topic_related_to_user(self.request))
        context['show_order'] = True
        context['get_top_thread_keywords'] = get_top_thread_keywords(self.request, 10)
        return context


def create_thread(request, topic_pk=None, nodegroup_pk=None):
    topic = None
    topics = Topic.objects.all()
    node_group = NodeGroup.objects.all()
    fixed_nodegroup = NodeGroup.objects.filter(pk=nodegroup_pk)
    if topic_pk:
        topic = Topic.objects.get(pk=topic_pk)
    if nodegroup_pk:
        topics = topics.filter(node_group=nodegroup_pk)
    topics = Topic.objects.filter(id__in=Topic_related_to_user(request))
    if request.method == 'POST':
        form = ThreadForm(request.POST, user=request.user)
        if form.is_valid():
            t = form.save()
            return HttpResponseRedirect(reverse('student_thread', kwargs={'pk': t.pk}))
    else:
        form = ThreadForm(user=request.user)

    return render(request, 'student_module/student_forum/create_thread.html',
                  {'form': form, 'node_group': node_group, 'title': _('Create Thread'), 'topic': topic,
                   'fixed_nodegroup': fixed_nodegroup, 'topics': topics})


import operator
from django.db.models import Q
from functools import reduce


def ThreadSearchAjax(request, topic_id, threadkeywordList):
    threadkeywordList = threadkeywordList.split("_")
    RelevantThread = []
    if topic_id:
        RelevantThread = Thread.objects.filter(topic=topic_id)
        pass
    else:
        RelevantTopics = Topic_related_to_user(request).values_list('pk')
        RelevantThread = Thread.objects.filter(topic__in=RelevantTopics)
        pass
    RelevantThread = RelevantThread.filter(reduce(operator.and_, (Q(title__contains=x) for x in threadkeywordList)))[:5]
    return render(request, 'student_module/student_forum/ThreadSearchAjax.html', {'RelevantThread': RelevantThread})


def create_topic(request, student_nodegroup_pk=None):
    node_group = NodeGroup.objects.filter(pk=student_nodegroup_pk)
    if request.method == 'POST':
        form = TopicForm(request.POST, user=request.user)
        if form.is_valid():
            t = form.save()
            return HttpResponseRedirect(reverse('student_topic', kwargs={'pk': t.pk}))
    else:
        form = TopicForm()

    return render(request, 'student_module/student_forum/create_topic.html',
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
    template_name = 'student_module/student_forum/search.html'
    context_object_name = 'threads'

    def get_queryset(self):
        keywords = self.kwargs.get('keyword')
        query = get_query(keywords, ['title'])
        return Thread.objects.visible().filter(
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
        return HttpResponseRedirect(reverse('student_search', kwargs={'keyword': keyword}))
    else:
        return HttpResponseForbidden('Post you cannot')


class NodeGroupView(ListView):
    model = Topic
    template_name = 'student_module/student_forum/nodegroup.html'
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
                thread = Thread.objects.visible().filter(
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
    template_name = 'student_module/student_forum/thread.html'
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
                reverse('student_thread', kwargs={'pk': thread_id})
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
    template_name = 'student_module/student_forum/topic.html'
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
    return render(request, 'student_module/student_forum/user_info.html', {
        'title': u.username,
        'user': u,
        'threads': u.threads.visible().select_related('topic')[:10],
        'replies': u.posts.visible().select_related('thread', 'user').order_by('-pub_date')[:30],
    })


class UserPosts(ListView):
    model = Post
    paginate_by = 15
    template_name = 'student_module/student_forum/user_replies.html'
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
    template_name = 'student_module/student_forum/user_threads.html'
    context_object_name = 'threads'

    def get_queryset(self):
        return Thread.objects.visible().filter(
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
    template_name = 'student_module/student_forum/notifications.html'
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
            return HttpResponseRedirect(reverse('student_thread', kwargs={'pk': t.pk}))
    else:
        form = ThreadEditForm(instance=thread)

    return render(request, 'student_module/student_forum/edit_thread.html',
                  {'form': form, 'object': thread, 'title': ('Edit thread')})


def CourseForum(request, course):
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

    return redirect('student_topic', pk=course_forum.pk)


def Topic_related_to_user(request, node_group=None):
    innings = InningInfo.objects.filter(Groups__in=GroupMapping.objects.filter(Students__pk=request.user.pk))
    if node_group == None:
        own_center_general_topic = Topic.objects.filter(center_associated_with=request.user.Center_Code,

                                                        course_associated_with__isnull=True) | Topic.objects.filter(
            center_associated_with__isnull=True, course_associated_with__isnull=True)
        assigned_topics = ''
        if innings:
            courses = InningGroup.objects.filter(inninginfo__in=innings).values_list('Course_Code__pk')
            own_courses_forum_topics = Topic.objects.filter(course_associated_with__in=courses)
            assigned_topics = own_courses_forum_topics | own_center_general_topic
        else:
            assigned_topics = own_center_general_topic
    else:
        own_center_general_topic = Topic.objects.filter(node_group=node_group.pk,
                                                        center_associated_with=request.user.Center_Code,
                                                        course_associated_with__isnull=True) | Topic.objects.filter(
            node_group=node_group.pk, center_associated_with__isnull=True, course_associated_with__isnull=True)
        if innings:
            courses = InningGroup.objects.filter(inninginfo__in=innings).values_list('Course_Code__pk')
            own_courses_forum_topics = Topic.objects.filter(node_group=node_group.pk,
                                                            course_associated_with__in=courses)
            assigned_topics = own_courses_forum_topics | own_center_general_topic
        else:
            assigned_topics = own_center_general_topic
    return assigned_topics


def Thread_related_to_user(request):
    return Thread.objects.filter(topic__in=Topic_related_to_user(request))


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


class QuizUserProgressView(TemplateView):
    template_name = 'student_quiz/progress.html'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(QuizUserProgressView, self) \
            .dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(QuizUserProgressView, self).get_context_data(**kwargs)
        progress, c = Progress.objects.get_or_create(user=self.request.user)
        # context['cat_scores'] = progress.list_all_cat_scores
        # context['exams'] = progress.show_exams()
        context['sittings'] = Sitting.objects.filter(user=self.request.user)
        return context


class QuizUserProgressDetailView(DetailView):
    template_name = 'student_quiz/progress_detail.html'
    model = Sitting

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


def PageUpdateAjax(request, course, chapter):
    if request.method == 'POST':
        jsondata = chapterProgressRecord(str(course), str(chapter), str(request.user.id),
                                         currentPageNumber=request.POST['currentpage'],
                                         totalPage=request.POST['totalpages'],
                                         fromcontents=True, studytimeinseconds=request.POST['studytimeinseconds'],
                                         )
    else:
        # currentPageNumber, totalpage = maintainLastPageofStudent(str(course), str(chapter), str(request.user.id),
        #                                                          )
        jsondata = chapterProgressRecord(str(course), str(chapter), str(request.user.id), fromcontents=True,
                                         currentPageNumber=None, totalPage=None,
                                         studytimeinseconds=None,
                                         )
    return JsonResponse(jsondata)


from django.contrib.auth import authenticate, login as auth_login

from django.shortcuts import redirect, reverse


def loginforapp(request, course, chapter, username, password):
    user = authenticate(username=username, password=password)
    if user is not None:
        auth_login(request, user)
        if request.user.is_authenticated:
            return redirect(
                "/students/courseinfo/" + str(course) + "/chapterinfo/" + str(
                    chapter) + "/contents" + '?mobileViewer=1',
            )
        else:
            return HttpResponse('failed')
    else:
        return HttpResponse('failed')


from django.db.models import F


@api_view(['GET', ])
@permission_classes((IsAuthenticated,))
def singleUserHomePageJSON(request):
    if request.user.Is_Student:
        courses = request.user.get_student_courses()
        assignments = AssignmentInfo.objects.filter(
            Course_Code__in=courses,
            Chapter_Code__Use_Flag=True)[:7]

        batches = GroupMapping.objects.filter(Students__id=request.user.id, Center_Code=request.user.Center_Code)
        sessions = []
        if batches:
            for batch in batches:
                # Filtering out only active sessions
                session = InningInfo.objects.filter(Groups__id=batch.id, End_Date__gt=datetime_now)
                sessions += session

        student_group = request.user.groupmapping_set.all()
        student_session = InningInfo.objects.filter(Groups__in=student_group)
        active_student_session = InningInfo.objects.filter(Groups__in=student_group, End_Date__gt=datetime_now)
        student_course = InningGroup.objects.filter(inninginfo__in=active_student_session).values("Course_Code")

        # Predefined category name "general, session, course, system"
        general_survey = SurveyInfo.objects.filter(Category_Code__Category_Name__iexact="general",
                                                   Center_Code=request.user.Center_Code, Use_Flag=True)
        session_survey = SurveyInfo.objects.filter(Category_Code__Category_Name__iexact="session",
                                                   Session_Code__in=student_session, Use_Flag=True)
        course_survey = SurveyInfo.objects.filter(Category_Code__Category_Name__iexact="course",
                                                  Course_Code__in=student_course, Use_Flag=True)
        system_survey = SurveyInfo.objects.filter(Center_Code=None, Use_Flag=True)

        sitting_queryset = Sitting.objects.filter(user=request.user, complete=True).order_by('-end')[:5]

        survey_queryset = general_survey | session_survey | course_survey | system_survey
        survey_queryset = survey_queryset.filter(End_Date__gte=timezone.now()).exclude(
            submitsurvey__Student_Code__pk__in=[request.user.pk, ])

        user = MemberInfo.objects.filter(pk=request.user.pk).values('pk', 'first_name', 'last_name', 'Member_Avatar',
                                                                    'email', 'username', 'Member_Permanent_Address',
                                                                    'Member_Temporary_Address', 'Member_BirthDate',
                                                                    'Member_Phone', 'Use_Flag', 'Is_Teacher',
                                                                    'Is_Student', 'Is_CenterAdmin', 'Member_Gender',
                                                                    'Center_Code')
        courses_list = courses.values(pk=F('Course_Code__pk'), Course_Name=F('Course_Code__Course_Name'),
                                      Course_Description=F('Course_Code__Course_Description'),
                                      Course_Cover_File=F('Course_Code__Course_Cover_File'),
                                      Course_Level=F('Course_Code__Course_Level'),
                                      Course_Info=F('Course_Code__Course_Info'), Use_Flag=F('Course_Code__Use_Flag'),
                                      Center_Code=F('Course_Code__Center_Code'),
                                      Register_Agent=F('Course_Code__Register_Agent'))
        assignments_list = assignments.values('id', 'Assignment_Topic', 'Use_Flag', 'Assignment_Deadline',
                                              'Register_DateTime',
                                              course_code=F('Course_Code__pk'),
                                              course_name=F('Course_Code__Course_Name'),
                                              chapter_code=F('Chapter_Code__pk'),
                                              Register_Agent_Username=F('Register_Agent__username'),
                                              Register_Agent_Firstname=F('Register_Agent__first_name'),
                                              Register_Agent_Lastname=F('Register_Agent__last_name'))
        survey_list = survey_queryset.values('id', 'Survey_Title', 'Start_Date', 'End_Date', 'Survey_Cover', 'Use_Flag',
                                             'Retaken_From', 'Version_No', 'Center_Code', 'Category_Code',
                                             'Session_Code', 'Course_Code', 'Added_By')
        sitting_list = sitting_queryset.values('pk', 'user', 'question_order', 'question_list', 'incorrect_questions',
                                               'current_score', 'complete', 'user_answers', 'start', 'end',
                                               'score_list', course_name=F('quiz__course_code__Course_Name'),
                                               course_pk=F('quiz__course_code__pk'), quiz_pk=F('quiz__pk'),
                                               quiz_title=F('quiz__title'), single_attempt=F('quiz__single_attempt'))

        for counter, assg in enumerate(assignments_list):
            questions = AssignmentQuestionInfo.objects.filter(Assignment_Code__pk=assg['id'])
            answers = AssignAnswerInfo.objects.filter(Question_Code__in=questions, Student_Code=request.user)
            if len(questions) == len(answers):
                assignments_list[counter].update({
                    'complete': True,
                    'question_count': questions.count(),
                    'answer_count': answers.count(),
                })
            else:
                assignments_list[counter].update({
                    'complete': False,
                    'question_count': questions.count(),
                    'answer_count': answers.count(),
                })

        response = {'userinfo': list(user), 'courses': list(courses_list), 'assignments': list(assignments_list),
                    'survey': list(survey_list), 'sitting': list(sitting_list)}
        return JsonResponse(response, safe=False, json_dumps_params={'indent': 2})
    else:
        HttpResponse('You are not a student.')
