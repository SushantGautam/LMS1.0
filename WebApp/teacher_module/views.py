from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.views import PasswordContextMixin
# from django.core.checks import messages
from django.contrib import messages
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters
from django.views.generic import ListView, CreateView, DetailView, UpdateView, FormView

from WebApp.forms import CourseInfoForm, ChapterInfoForm, AssignmentInfoForm
from WebApp.models import CourseInfo, ChapterInfo, InningInfo, QuestionInfo, AssignmentInfo, MemberInfo, InningGroup
from survey.models import SurveyInfo
from quiz.models import Question , Quiz
from datetime import datetime
from forum.models import NodeGroup, Thread, Topic
from forum.views import get_top_thread_keywords
from .forms import ThreadForm
datetime_now = datetime.now()

def start(request):
    """Start page with a documentation.
    """
    # return render(request,"start.html")

    if request.user.Is_Teacher: 
        mycourse = InningGroup.objects.filter(Teacher_Code=request.user.id, Center_Code=request.user.Center_Code)
        sessions = []
        if mycourse:
            for course in mycourse:
                session = InningInfo.objects.filter(Course_Group=course.id,End_Date__gt=datetime_now)
                sessions += session
        courseID=[]
        for groups in mycourse:
            courseID.append(groups.Course_Code.id)
     
        activeassignments = []   
        for course in courseID:
            activeassignments += AssignmentInfo.objects.filter(Register_Agent=request.user.id,Course_Code=course,Assignment_Deadline__gte=datetime_now)
        
        return render(request, "teacher_module/homepage.html",{'MyCourses':mycourse,'Session':sessions,'activeAssignments':activeassignments})

  
       
     

def Dashboard(request):
    return render(request, 'teacher_module/homepage.html', )

class MyCourseListView(ListView):
    model = CourseInfo
    template_name = 'teacher_module/mycourses.html'

    paginate_by = 8

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['courses'] = InningGroup.objects.filter(Teacher_Code=self.request.user.id, Center_Code=self.request.user.Center_Code)

        sessions = []
        if context['courses']:
            for course in context['courses']: 
                # Filtering out only active sessions
                session = InningInfo.objects.filter(Groups__id=course.id,End_Date__gt=datetime_now)
                sessions += session
        context['sessions'] = sessions
        # courses = set()
        # if context['sessions']:
        #     for session in context['sessions']:
        #         course = session.Course_Group.all()
        #         courses.update(course)
        # context['Course'] = courses

        return context

    def get_queryset(self):
        qsearch = self.model.objects.all()

        query = self.request.GET.get('teacher_mycoursequery')
        if query:
            query=query.strip()
            qsearch = qsearch.filter(Course_Name__contains=query)
            if not len(qsearch):
                messages.error(self.request, 'Sorry no course found! Try with a different keyword')
        qsearch = qsearch.order_by("-id")  # you don't need this if you set up your ordering on the model
        return qsearch

class CourseInfoListView(ListView):
    model = CourseInfo
    template_name = 'teacher_module/courseinfo_list.html'
    paginate_by = 8


    def get_queryset(self):
        qs = self.model.objects.all()

        query = self.request.GET.get('teacher_coursequery')
        if query:
            query = query.strip()
            qs = qs.filter(Course_Name__contains=query)
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
        return reverse_lazy('teacher_courseinfo_detail', kwargs = {'pk': self.object.pk})

class CourseInfoDetailView(DetailView):
    model = CourseInfo
    template_name = 'teacher_module/courseinfo_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['chapters'] = ChapterInfo.objects.filter(Course_Code=self.kwargs.get('pk')).order_by('Chapter_No')
        context['surveycount'] = SurveyInfo.objects.filter(Course_Code=self.kwargs.get('pk')).count()
        context['quizcount'] = Question.objects.filter(course_code=self.kwargs.get('pk')).count()
        return context


class CourseInfoUpdateView(UpdateView):
    model = CourseInfo
    form_class = CourseInfoForm
    template_name = 'teacher_module/courseinfo_form.html'
    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['Course_Code'] = get_object_or_404(CourseInfo, pk=self.kwargs.get('course'))
    #     return context
    def get_success_url(self, **kwargs):
        return reverse_lazy('teacher_courseinfo_detail', kwargs = {'pk': self.object.pk})

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
    

class ChapterInfoDetailView(DetailView):
    model = ChapterInfo
    template_name = 'teacher_module/chapterinfo_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['assignments'] = AssignmentInfo.objects.filter(Chapter_Code=self.kwargs.get('pk')) 
        context['quizes'] = Quiz.objects.filter(chapter_code=self.kwargs.get('pk'))
        return context

def ChapterInfoBuildView(request):
    return render(request, 'teacher_module/coursebuilder.html')


class ChapterInfoUpdateView(UpdateView):
    model = ChapterInfo
    form_class = ChapterInfoForm
    template_name = 'teacher_module/chapterinfo_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['Course_Code'] = get_object_or_404(CourseInfo, pk=self.kwargs.get('course'))
        return context

class AssignmentInfoDetailView(DetailView):
    model = AssignmentInfo
    template_name = 'teacher_module/assignmentinfo_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['Questions'] = QuestionInfo.objects.filter(Assignment_Code=self.kwargs.get('pk'))
        context['Course_Code'] = get_object_or_404(CourseInfo, pk=self.kwargs.get('course'))
        context['Chapter_No'] = get_object_or_404(ChapterInfo, pk=self.kwargs.get('chapter'))
        # context['Assignment_Code'] = get_object_or_404(AssignmentInfo, pk=self.kwargs.get('assignment'))
        return context

class AssignmentInfoUpdateView(UpdateView):
    model = AssignmentInfo
    form_class = AssignmentInfoForm
    template_name = 'teacher_module/assignmentinfo_form.html'


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
        courseID=[]
        for groups in context['Group']:
            courseID.append(groups.Course_Code.id)
        context['assignments'] = []
        context['expiredassignments'] = []
        context['activeassignments'] = []
        for course in courseID:
            context['assignments'] += AssignmentInfo.objects.filter(Register_Agent=self.request.user.id,Course_Code=course)
            context['expiredassignments'] += AssignmentInfo.objects.filter(Register_Agent=self.request.user.id,Course_Code=course,Assignment_Deadline__lt=datetime_now)
            context['activeassignments'] += AssignmentInfo.objects.filter(Register_Agent=self.request.user.id,Course_Code=course,Assignment_Deadline__gte=datetime_now)

        return context

def ProfileView(request):
    return render(request, 'teacher_module/profile.html')


def makequery(request):
    # model=SurveyInfo
    Course = CourseInfo.objects.all()
    Session = InningInfo.objects.all()
    return render(request, 'teacher_module/makequery.html', {
        'courses': Course,
        'sessions': Session
    })


def question_teachers(request):
    return render(request, 'teacher_module/question_teachers.html')


def polls_teachers(request):
    return render(request, 'teacher_module/polls_teachers.html')



# ___________________________________________________FORUM____________________________________
class Index(ListView):
    model = Thread
    template_name = 'teacher_module/forum/forumIndex.html'
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
            return HttpResponseRedirect(reverse('forum:thread', kwargs={'pk': t.pk}))
    else:
        form = ThreadForm()

    return render(request, 'teacher_module/forum/create_thread.html',
                  {'form': form, 'node_group': node_group, 'title': ('Create Thread'), 'topic': topic,
                   'fixed_nodegroup': fixed_nodegroup, 'topics': topics})
