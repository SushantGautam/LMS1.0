from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.views import PasswordContextMixin
# from django.core.checks import messages
from django.contrib import messages
from django.db import transaction
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters
from django.views.generic import ListView, CreateView, DetailView, UpdateView, FormView, TemplateView
from django_addanother.views import CreatePopupMixin

from WebApp.forms import CourseInfoForm, ChapterInfoForm, AssignmentInfoForm
from WebApp.models import CourseInfo, ChapterInfo, InningInfo, QuestionInfo, AssignmentInfo, MemberInfo, InningGroup
from quiz.forms import SAQuestionForm, QuizForm, QuestionForm, AnsFormset, MCQuestionForm, TFQuestionForm
from quiz.views import QuizMarkerMixin, SittingFilterTitleMixin
from survey.models import SurveyInfo
from quiz.models import Question, Quiz, SA_Question, Sitting, MCQuestion, TF_Question
from datetime import datetime
from forum.models import NodeGroup, Thread, Topic
from forum.views import get_top_thread_keywords
from .forms import ThreadForm
datetime_now = datetime.now()

from formtools.wizard.views import SessionWizardView
from quiz.forms import QuizForm1, QuizForm2, QuizForm3

from quiz.models import Progress

from django.urls import reverse

from django.http import JsonResponse, HttpResponseRedirect

from django.core.exceptions import ValidationError
from django.http import HttpResponse

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
    template_name = 'teacher_module/quiz_list.html'

    def get_queryset(self):
        queryset = super(QuizListView, self).get_queryset()
        return queryset.filter(draft=False, cent_code=self.request.user.Center_Code)


class QuizUpdateView(UpdateView):
    model = Quiz
    form_class = QuizForm


class QuizDetailView(DetailView):
    model = Quiz
    slug_field = 'url'
    template_name = 'teacher_module/quiz_detail.html'

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


class QuizMarkingList(QuizMarkerMixin, SittingFilterTitleMixin, ListView):
    model = Sitting

    def get_queryset(self):
        queryset = super(QuizMarkingList, self).get_queryset() \
            .filter(complete=True)

        user_filter = self.request.GET.get('user_filter')
        if user_filter:
            queryset = queryset.filter(user__username__icontains=user_filter)

        return queryset


class QuizMarkingDetail(QuizMarkerMixin, DetailView):
    model = Sitting

    def post(self, request, *args, **kwargs):
        sitting = self.get_object()

        q_to_toggle = request.POST.get('qid', None)
        if q_to_toggle:
            q = Question.objects.get_subclass(id=int(q_to_toggle))
            if int(q_to_toggle) in sitting.get_incorrect_questions:
                sitting.remove_incorrect_question(q)
            else:
                sitting.add_incorrect_question(q)

        return self.get(request)

    def get_context_data(self, **kwargs):
        context = super(QuizMarkingDetail, self).get_context_data(**kwargs)
        context['questions'] = \
            context['sitting'].get_questions(with_answers=True)
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

TEMPLATES = {"form1": "wizard_teacher/step1.html",
             "form2": "wizard_teacher/step2.html",
             "form3": "wizard_teacher/step3.html"}


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
            form.fields["course_code"].queryset = CourseInfo.objects.filter(Center_Code=self.request.user.Center_Code)

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
