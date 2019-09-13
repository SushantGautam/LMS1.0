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

from WebApp.forms import CourseInfoForm, ChapterInfoForm
from WebApp.models import CourseInfo, ChapterInfo, InningInfo, QuestionInfo, AssignmentInfo, MemberInfo
from survey.models import SurveyInfo
from quiz.models import Question , Quiz


def start(request):
    """Start page with a documentation.
    """
    # return render(request,"start.html")

    return render(request, "teacher_module/homepage.html")


def Dashboard(request):
    return render(request, 'teacher_module/homepage.html', )


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


class ChapterInfoListView(ListView):
    model = ChapterInfo
    template_name = 'teacher_module/chapterinfo_list.html'


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

class MyAssignmentsListView(ListView):
    model = AssignmentInfo
    template_name = 'teacher_module/myassignments_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['currentDate'] = datetime.now()
        context['GroupName'] = GroupMapping.objects.get(Students__id=self.request.user.id)
        context['Group'] = InningInfo.objects.get(Groups__id=context['GroupName'].id)
        context['Course'] = context['Group'].Course_Group.all()

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
