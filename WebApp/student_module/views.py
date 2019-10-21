# from django.shortcuts import render
#
#
# def start(request):
#     """Start page with a documentation.
#     """
#     # return render(request,"start.html")
#     return render(request, "student_module/homepage.html")

from datetime import datetime

from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.views import PasswordContextMixin
from django.http import JsonResponse
from django.shortcuts import redirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.utils.translation import gettext as _
from django.views import View
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters
# Create your views here.
from django.views.generic import ListView, CreateView, DetailView, UpdateView, TemplateView
from django.views.generic.edit import FormView
from forum.models import NodeGroup, Thread, Topic, Post, Notification
from forum.views import get_top_thread_keywords
from forum.forms import ThreadForm, TopicForm, ReplyForm, ThreadEditForm
from WebApp.forms import UserUpdateForm
from WebApp.models import CourseInfo, GroupMapping, InningInfo, ChapterInfo, AssignmentInfo, MemberInfo, \
    AssignmentQuestionInfo, \
    AssignAnswerInfo
from quiz.models import Question, Quiz
from survey.models import SurveyInfo, CategoryInfo, OptionInfo, SubmitSurvey, AnswerInfo, QuestionInfo
from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.contrib.auth import get_user_model
from .misc import get_query
from LMS import settings
import uuid
from django.core.files.storage import FileSystemStorage
from WebApp.filters import MyCourseFilter
from django.core.paginator import Paginator , EmptyPage, PageNotAnInteger

datetime_now = datetime.now()


User = get_user_model()


def start(request):
    if request.user.Is_Student:
        batches = GroupMapping.objects.filter(
            Students__id=request.user.id, Center_Code=request.user.Center_Code)
        sessions = []
        if batches:
            for batch in batches:
                # Filtering out only active sessions
                session = InningInfo.objects.filter(
                    Groups__id=batch.id, End_Date__gt=datetime_now)
                sessions += session
        # courses = []
        # activeassignments = []
        # if sessions:
        #     for session in sessions:
        #         courses.append(session.Course_Group)
        courses = set()
        activeassignments = []
        if sessions:
            for session in sessions:
                course = session.Course_Group.all()
                courses.update(course)
            for course in courses:
                activeassignments += AssignmentInfo.objects.filter(
                    Assignment_Deadline__gte=datetime_now, Course_Code=course.Course_Code.id)[:7]

        return render(request, 'student_module/dashboard.html',
                      {'GroupName': batches, 'Group': sessions, 'Course': courses, 'activeAssignments': activeassignments})


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
    return render(request, 'student_module/calendar.html')


class MyCoursesListView(ListView):
    model = CourseInfo
    template_name = 'student_module/myCourse.html'

    # paginate_by = 8

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['batches'] = GroupMapping.objects.filter(
            Students__id=self.request.user.id, Center_Code=self.request.user.Center_Code)

        sessions = []
        if context['batches']:
            for batch in context['batches']:
                # Filtering out only active sessions
                session = InningInfo.objects.filter(
                    Groups__id=batch.id, End_Date__gt=datetime_now)
                sessions += session
        context['sessions'] = sessions
        courses = set()
        if context['sessions']:
            for session in context['sessions']:
                course = session.Course_Group.all()
                courses.update(course)
        context['Course'] = courses
        filtered_qs = MyCourseFilter(
                      self.request.GET, 
                      queryset=course
                  ).qs
        paginator = Paginator(filtered_qs, 8)
        page = self.request.GET.get('page')
        try:
            response = paginator.page(page)
        except PageNotAnInteger:
            response = paginator.page(1)
        except EmptyPage:
            response = paginator.page(paginator.num_pages)
        context['response'] = response
        context['paginator'] = paginator
        context['page'] = page
        # context['filtered_qs'] = filtered_qs


        return context

    def get_queryset(self):
        qset = self.model.objects.all()
        queryset = self.request.GET.get('studentmycoursequery')
        if queryset:
            queryset = queryset.strip()
            qset = qset.filter(Course_Name__contains=queryset)
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
        context['currentDate'] = datetime.now()
        context['GroupName'] = []
        context['GroupName'] += GroupMapping.objects.filter(
            Students__id=self.request.user.id)
        context['Group'] = []
        for group in context['GroupName']:
            context['Group'] += InningInfo.objects.filter(Groups__id=group.id)
        context['Course'] = []
        context['Assignment'] = []
        context['activeAssignment'] = []
        context['expiredAssignment'] = []
        for course in context['Group']:
            Assignment = []
            activeAssignment = []
            expiredAssignment = []
            context['Course'] += course.Course_Group.all()

            for assignment in context['Course']:
                Assignment.append(AssignmentInfo.objects.filter(
                    Course_Code__id=assignment.Course_Code.id))
                activeAssignment.append(AssignmentInfo.objects.filter(
                    Course_Code__id=assignment.Course_Code.id, Assignment_Deadline__gte=datetime_now))
                expiredAssignment.append(AssignmentInfo.objects.filter(
                    Course_Code__id=assignment.Course_Code.id, Assignment_Deadline__lte=datetime_now))
                # print(context['Assignment'])
            context['Assignment'].append(Assignment)
            context['activeAssignment'].append(activeAssignment)
            context['expiredAssignment'].append(expiredAssignment)
        return context


class CourseInfoListView(ListView):
    model = CourseInfo
    template_name = 'student_module/courseinfo_list.html'

    paginate_by = 8

    def get_queryset(self):
        qs = self.model.objects.all()

        query = self.request.GET.get('coursequery')
        if query:
            query = query.strip()
            qs = qs.filter(Course_Name__contains=query)
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
            Course_Code=self.kwargs.get('pk')).order_by('Chapter_No')
        context['surveycount'] = SurveyInfo.objects.filter(
            Course_Code=self.kwargs.get('pk'))
        context['quizcount'] = Question.objects.filter(
            course_code=self.kwargs.get('pk'))
        context['topic'] = Topic.objects.filter(course_associated_with=self.kwargs.get('pk'))
        return context


class ChapterInfoListView(ListView):
    model = ChapterInfo


class ChapterInfoDetailView(DetailView):
    model = ChapterInfo
    template_name = 'student_module/chapterinfo_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['assignments'] = AssignmentInfo.objects.filter(
            Chapter_Code=self.kwargs.get('pk'))
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
        Obj = AssignAnswerInfo()
        Obj.Assignment_Answer = request.POST["Assignment_Answer"]
        Obj.Student_Code = MemberInfo.objects.get(
            pk=request.POST["Student_Code"])
        Obj.Question_Code = AssignmentQuestionInfo.objects.get(
            pk=request.POST["Question_Code"])
        Assignment_Code = Obj.Question_Code.Assignment_Code
        if bool(request.FILES.get('Assignment_File',False)) == True:
            media = request.FILES['Assignment_File']
            # print(media)
            if media.size / 1024 > 2048:
                return JsonResponse(data={'status':'Fail',"msg": "File size exceeds 2MB"}, status=500)
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

        context['options'] = OptionInfo.objects.all()
        context['submit'] = SubmitSurvey.objects.all()

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
        # print(request.POST)
        submitSurvey = SubmitSurvey()
        submitSurvey.Survey_Code = SurveyInfo.objects.get(id=surveyId)
        submitSurvey.Student_Code = MemberInfo.objects.get(id=userId)
        submitSurvey.save()

        for question in QuestionInfo.objects.filter(Survey_Code=surveyId):

            optionId = request.POST[str(question.id)]
            answerObject = AnswerInfo()
            answerObject.Answer_Value = optionId
            answerObject.Question_Code = question
            answerObject.Submit_Code = submitSurvey
            answerObject.save()

        return redirect('questions_student')


class surveyFilterCategory_student(ListView):
    model = SurveyInfo
    template_name = 'student_module/questions_student_listView.html'

    def get_queryset(self):
        # print(self.request.GET['categoryId'])
        # print(SurveyInfo.objects.filter(Category_Code = self.request.GET['categoryId']))
        if self.request.GET['categoryId'] == '0':

            return SurveyInfo.objects.all()
            # filter(Center_Code = self.request.user.Center_Code)
        else:
            return SurveyInfo.objects.filter(Category_Code=self.request.GET['categoryId'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['currentDate'] = datetime.now()

        submitSurveyQuerySet = SubmitSurvey.objects.filter(
            Student_Code=self.request.user.id)
        context['submittedSurvey'] = [
            el.Survey_Code.id for el in submitSurveyQuerySet]

        return context


class Index(ListView):
    model = Thread
    template_name = 'student_module/student_forum/forumIndex.html'
    context_object_name = 'threads'

    def get_queryset(self):
        nodegroups = NodeGroup.objects.all()
        threadqueryset = Thread.objects.none()
        for ng in nodegroups:
            topics = Topic.objects.filter(node_group=ng.pk)
            for topic in topics:
                threads = Thread.objects.visible().filter(
                    topic=topic.pk).order_by('pub_date')[:4]
                threadqueryset |= threads

        return threadqueryset

    def get_context_data(self, **kwargs):
        context = super(ListView, self).get_context_data(**kwargs)
        context['panel_title'] = ('New Threads')
        context['title'] = ('Index')
        context['topics'] = Topic.objects.all()
        context['show_order'] = True
        context['get_top_thread_keywords'] = get_top_thread_keywords(
            self.request, 10)
        return context


def create_thread(request, topic_pk=None, nodegroup_pk=None):
    topic = None
    node_group = NodeGroup.objects.all()
    fixed_nodegroup = NodeGroup.objects.filter(pk=nodegroup_pk)
    if topic_pk:
        topic = Topic.objects.get(pk=topic_pk)
    topics = Topic.objects.filter(node_group=nodegroup_pk)
    if request.method == 'POST':
        form = ThreadForm(request.POST, user=request.user)
        if form.is_valid():
            t = form.save()
            return HttpResponseRedirect(reverse('student_thread', kwargs={'pk': t.pk}))
    else:
        form = ThreadForm()

    return render(request, 'student_module/student_forum/create_thread.html',
                  {'form': form, 'node_group': node_group, 'title': _('Create Thread'), 'topic': topic,
                   'fixed_nodegroup': fixed_nodegroup, 'topics': topics})


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
    paginate_by = 20
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
        )

    def get_context_data(self, **kwargs):
        context = super(ListView, self).get_context_data(**kwargs)
        context['title'] = context['panel_title'] = (
            'Search: ') + self.kwargs.get('keyword')
        context['show_order'] = True
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
        )

    def get_context_data(self, **kwargs):
        topics = Topic.objects.filter(node_group__id=self.kwargs.get('pk'))
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
            # print("sabina", latest_threads)
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
    template_name = 'student_module/student_forum/thread.html'
    context_object_name = 'posts'

    def get_queryset(self):
        return Post.objects.filter(
            thread_id=self.kwargs.get('pk')
        ).select_related(
            'user'
        ).prefetch_related(
            'user__forum_avatar'
        ).order_by('pub_date')

    def get_context_data(self, **kwargs):
        context = super(ListView, self).get_context_data(**kwargs)
        current = Thread.objects.get(pk=self.kwargs.get('pk'))
        current.increase_view_count()
        context['thread'] = current
        context['title'] = context['thread'].title
        context['topic'] = context['thread'].topic
        context['form'] = ReplyForm()
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

    return render(request, 'student_module/student_forum/edit_thread.html', {'form': form, 'object': thread, 'title': ('Edit thread')})


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
        Topic.objects.create(title=course.Course_Name, node_group=course_node_forum, course_associated_with=course).save()
        course_forum = Topic.objects.get(course_associated_with=course)
    return redirect('student_topic', pk=course_forum.pk)




