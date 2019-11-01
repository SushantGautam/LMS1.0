# from django.core.checks import messages
from datetime import datetime

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
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.utils.translation import gettext as _
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters
from django.views.generic import ListView, CreateView, DetailView, UpdateView, TemplateView, DeleteView
from django.views.generic.edit import FormView
from django_addanother.views import CreatePopupMixin

from WebApp.forms import CourseInfoForm, ChapterInfoForm, AssignmentInfoForm
from WebApp.forms import UserUpdateForm
from WebApp.models import CourseInfo, ChapterInfo, InningInfo, AssignmentQuestionInfo, AssignmentInfo, InningGroup, \
    AssignAnswerInfo, MemberInfo, GroupMapping
from forum.forms import ThreadForm, ThreadEditForm
from forum.models import NodeGroup, Thread, Topic
from forum.models import Post, Notification
from forum.views import get_top_thread_keywords
from quiz.forms import SAQuestionForm, QuizForm, QuestionForm, AnsFormset, MCQuestionForm, TFQuestionForm
from quiz.models import Question, Quiz, SA_Question, Sitting, MCQuestion, TF_Question
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

from WebApp.filters import MyCourseFilter
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

User = get_user_model()


def start(request):
    """Start page with a documentation.
    """
    # return render(request,"start.html")

    if request.user.Is_Teacher:
        mycourse = InningGroup.objects.filter(Teacher_Code=request.user.id, Center_Code=request.user.Center_Code)
        sessions = []
        if mycourse:
            for course in mycourse:
                session = InningInfo.objects.filter(Course_Group=course.id, End_Date__gt=datetime_now)
                sessions += session
        courseID = []
        for groups in mycourse:
            courseID.append(groups.Course_Code.id)

        activeassignments = []
        for course in courseID:
            activeassignments += AssignmentInfo.objects.filter(Register_Agent=request.user.id, Course_Code=course,
                                                               Assignment_Deadline__gte=datetime_now)

        return render(request, "teacher_module/homepage.html",
                      {'MyCourses': mycourse, 'Session': sessions, 'activeAssignments': activeassignments})


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


class GroupMappingDetailViewTeacher(DetailView):
    model = GroupMapping
    template_name = 'teacher_module/groupmapping_detail.html'


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

    # paginate_by = 8

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        courses = InningGroup.objects.filter(Teacher_Code=self.request.user.id,
                                             Center_Code=self.request.user.Center_Code)
        context['courses'] = courses
        sessions = []
        if context['courses']:
            for course in context['courses']:
                # Filtering out only active sessions
                session = InningInfo.objects.filter(Groups__id=course.id, End_Date__gt=datetime_now)
                sessions += session
        context['sessions'] = sessions
        
        filtered_qs = MyCourseFilter(
            self.request.GET,
            queryset=courses
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
       

        return context

    def get_queryset(self):
        qsearch = self.model.objects.all()

        query = self.request.GET.get('teacher_mycoursequery')
        if query:
            query = query.strip()
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
        return reverse_lazy('teacher_courseinfo_detail', kwargs={'pk': self.object.pk})


class CourseInfoDetailView(DetailView):
    model = CourseInfo
    template_name = 'teacher_module/courseinfo_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['chapters'] = ChapterInfo.objects.filter(Course_Code=self.kwargs.get('pk')).order_by('Chapter_No')
        context['surveycount'] = SurveyInfo.objects.filter(Course_Code=self.kwargs.get('pk'))
        context['quizcount'] = Question.objects.filter(course_code=self.kwargs.get('pk'))
        context['topic'] = Topic.objects.filter(course_associated_with=self.kwargs.get('pk'))
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

    def get_success_url(self, **kwargs):
        return reverse_lazy('teacher_chapterinfo_detail',
                            kwargs={'course': self.object.Course_Code.id, 'pk': self.object.pk})


class ChapterInfoDetailView(DetailView):
    model = ChapterInfo
    template_name = 'teacher_module/chapterinfo_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['assignments'] = AssignmentInfo.objects.filter(Chapter_Code=self.kwargs.get('pk'))
        context['quizes'] = Quiz.objects.filter(chapter_code=self.kwargs.get('pk'))
        context['datetime'] = datetime.now()

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

    def get_success_url(self, **kwargs):
        return reverse_lazy('teacher_chapterinfo_detail',
                            kwargs={'course': self.object.Course_Code.id, 'pk': self.object.pk})


class AssignmentInfoDetailView(DetailView):
    model = AssignmentInfo
    template_name = 'teacher_module/assignmentinfo_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['Questions'] = AssignmentQuestionInfo.objects.filter(Assignment_Code=self.kwargs.get('pk'),
                                                                     Register_Agent=self.request.user.id)
        context['Course_Code'] = get_object_or_404(CourseInfo, pk=self.kwargs.get('course'))
        context['Chapter_No'] = get_object_or_404(ChapterInfo, pk=self.kwargs.get('chapter'))
        context['datetime'] = datetime.now()

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


class AssignmentAnswers(ListView):
    model = AssignAnswerInfo
    template_name = 'teacher_module/assignment_answers.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        questions = AssignmentQuestionInfo.objects.filter(Assignment_Code=self.kwargs['pk'],
                                                          Register_Agent=self.request.user.id)
        context['questions'] = questions
        context['Answers'] = AssignAnswerInfo.objects.filter(Question_Code__in=questions)
        context['Assignment'] = AssignmentInfo.objects.get(pk=self.kwargs['pk'])
        # context['Chapter_No'] = get_object_or_404(ChapterInfo, pk=self.kwargs.get('chapter'))
        # context['Assignment_Code'] = get_object_or_404(AssignmentInfo, pk=self.kwargs.get('assignment'))
        return context


class AssignmentInfoUpdateView(UpdateView):
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
        for groups in context['Group']:
            course.append(groups.Course_Code.id)
        Assignment = []
        expiredAssignment = []
        activeAssignment = []
        for course in course:
            Assignment.append(AssignmentInfo.objects.filter(Register_Agent=self.request.user.id, Course_Code=course))
            expiredAssignment.append(
                AssignmentInfo.objects.filter(Register_Agent=self.request.user.id, Course_Code=course,
                                              Assignment_Deadline__lt=datetime_now))
            activeAssignment.append(
                AssignmentInfo.objects.filter(Register_Agent=self.request.user.id, Course_Code=course,
                                              Assignment_Deadline__gte=datetime_now))
        context['Assignment'].append(Assignment)
        context['activeAssignment'].append(activeAssignment)
        context['expiredAssignment'].append(expiredAssignment)
        return context


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
    template_name = 'teacher_module/teacherSurveyInfo_ajax.html'
    success_url = reverse_lazy('question_teachers')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['questioninfo_formset'] = QuestionInfoFormset(self.request.POST, prefix='questioninfo')  # MCQ
            context['questionansinfo_formset'] = QuestionAnsInfoFormset(self.request.POST,
                                                                        prefix='questionansinfo')  # SAQ
        else:
            context['questioninfo_formset'] = QuestionInfoFormset(prefix='questioninfo')
            context['questionansinfo_formset'] = QuestionAnsInfoFormset(prefix='questionansinfo')
            context['categoryObject'] = CategoryInfo.objects.get(id=self.request.GET['categoryId'])
        return context

    def form_valid(self, form):
        vform = super().form_valid(form)
        context = self.get_context_data()
        qn = context['questioninfo_formset']
        qna = context['questionansinfo_formset']
        with transaction.atomic():
            if qn.is_valid():
                qn.instance = self.object
                qn.save()
            if qna.is_valid():
                qna.instance = self.object
                qna.save()
        return vform

    def get_form_kwargs(self):
        default_kwargs = super().get_form_kwargs()
        default_kwargs['center_code_id'] = self.request.user.Center_Code.id
        return default_kwargs


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
    template_name = 'quiz/teacher_quiz/quiz_list.html'

    def get_queryset(self):
        queryset = super(QuizListView, self).get_queryset()
        return queryset.filter(draft=False, cent_code=self.request.user.Center_Code)


class QuizUpdateView(UpdateView):
    model = Quiz
    form_class = QuizForm


class QuizDetailView(DetailView):
    model = Quiz
    slug_field = 'url'
    template_name = 'quiz/teacher_quiz/quiz_detail.html'

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
    template_name = 'teacher_module/sitting_list.html'

    def get_queryset(self):
        queryset = super(QuizMarkingList, self).get_queryset() \
            .filter(complete=True)

        user_filter = self.request.GET.get('user_filter')
        if user_filter:
            queryset = queryset.filter(user__username__icontains=user_filter)

        return queryset


class QuizMarkingDetail(QuizMarkerMixin, DetailView):
    model = Sitting
    template_name = 'teacher_module/sitting_detail.html'

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


class teacherSurveyFilterCategory(ListView):
    model = SurveyInfo
    template_name = 'survey/common/surveyinfo_expireView.html'

    def get_queryset(self):
        if self.request.GET['categoryId'] == '0':
            return SurveyInfo.objects.all()
        else:
            return SurveyInfo.objects.filter(Category_Code=self.request.GET['categoryId'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['currentDate'] = datetime.now()
        return context


class TeacherSurveyInfoDetailView(DetailView):
    model = SurveyInfo
    template_name = 'teacher_module/survey/surveyinfodetail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['questions'] = QuestionInfo.objects.filter(
            Survey_Code=self.kwargs.get('pk')).order_by('pk')
        context['options'] = OptionInfo.objects.all()
        context['submit'] = SubmitSurvey.objects.all()
        return context



# ___________________________________________________FORUM____________________________________

class Index(LoginRequiredMixin, ListView):
    model = Thread
    template_name = 'teacher_module/teacher_forum/forumIndex.html'
    context_object_name = 'threads'

    def get_queryset(self):
        nodegroups = NodeGroup.objects.all()
        threadqueryset = Thread.objects.none()
        for ng in nodegroups:
            topics = Topic.objects.filter(node_group=ng.pk).filter(id__in=Topic_related_to_user(self.request))
            for topic in topics:
                threads = Thread.objects.visible().filter(topic=topic.pk).order_by('pub_date').filter(
                    topic_id__in=Topic_related_to_user(self.request))[:4]
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



@login_required
def create_thread(request, topic_pk=None, nodegroup_pk=None):
    topic = None
    node_group = NodeGroup.objects.all()
    fixed_nodegroup = NodeGroup.objects.filter(pk=nodegroup_pk)
    if topic_pk:
        topic = Topic.objects.get(pk=topic_pk)
    topics = Topic.objects.filter(node_group=nodegroup_pk).filter(id__in=Topic_related_to_user(request))
    if request.method == 'POST':
        form = ThreadForm(request.POST, user=request.user)
        if form.is_valid():
            t = form.save()
            return HttpResponseRedirect(reverse('teacher_thread', kwargs={'pk': t.pk}))
    else:
        form = ThreadForm()

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

from forum.views import SearchView
class SearchView(SearchView):
    template_name = 'teacher_module/teacher_forum/search.html'
    
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
                reverse('teacher_thread', kwargs={'pk': thread_id})
            )


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
    except ObjectDoesNfotExist:
        NodeGroup.objects.create(title='Course', description='Root node for course Forum').save()
        course_node_forum = NodeGroup.objects.get(title='Course')

    try:
        course_forum = Topic.objects.get(course_associated_with=course)
    except ObjectDoesNotExist:
        Topic.objects.create(title=course.Course_Name, node_group=course_node_forum, course_associated_with=course,
                             center_associated_with=request.user.Center_Code, topic_icon="book").save()
        course_forum = Topic.objects.get(course_associated_with=course)
    
    return redirect('teacher_topic', pk=course_forum.pk)


def Topic_related_to_user(request):
    own_center_general_topic = Topic.objects.filter(center_associated_with=request.user.Center_Code).filter(
        course_associated_with__isnull=True)
    innings_Course_Code = InningGroup.objects.filter(Teacher_Code=request.user.id).values('Course_Code')
    return Topic.objects.filter(course_associated_with__in=innings_Course_Code) | own_center_general_topic


def Thread_related_to_user(request):
    # print("asigned threads", Thread.objects.filter(topic__in=Topic_related_to_user(request)))
    return Thread.objects.filter(topic__in=Topic_related_to_user(request))
