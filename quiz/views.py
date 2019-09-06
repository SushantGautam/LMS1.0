import random

from django_addanother.views import CreatePopupMixin

from django.contrib.auth.decorators import login_required, permission_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, render, redirect
from django.utils.decorators import method_decorator
from django.views.generic import DetailView, ListView, TemplateView, FormView, CreateView, UpdateView
from django.urls import reverse, reverse_lazy
from django.db import transaction

from WebApp.models import CourseInfo
from .forms import QuestionForm, SAForm, QuizForm, TFQuestionForm, SAQuestionForm, MCQuestionForm, AnsFormset
from .models import Quiz, Progress, Sitting, MCQuestion, TF_Question, Question, SA_Question, Answer


class QuizMarkerMixin(object):
    @method_decorator(login_required)
    @method_decorator(permission_required('quiz.view_sittings'))
    def dispatch(self, *args, **kwargs):
        return super(QuizMarkerMixin, self).dispatch(*args, **kwargs)


class SittingFilterTitleMixin(object):
    def get_queryset(self):
        queryset = super(SittingFilterTitleMixin, self).get_queryset()
        quiz_filter = self.request.GET.get('quiz_filter')
        if quiz_filter:
            queryset = queryset.filter(quiz__title__icontains=quiz_filter)

        return queryset

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
    #template_name = 'quiz/test_temp.html'
    model = Quiz
    #fields = ['title']
    form_class = QuizForm
    success_url = reverse_lazy('quiz_list')



class QuizListView(ListView):
    model = Quiz

    def get_queryset(self):
        queryset = super(QuizListView, self).get_queryset()
        return queryset.filter(draft=False)


class QuizUpdateView(UpdateView):
    model = Quiz
    form_class = QuizForm


class QuizDetailView(DetailView):
    model = Quiz
    slug_field = 'url'

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
    return redirect("quiz_list")


class CategoriesListView(ListView):
    model = CourseInfo


class ViewQuizListByCourse(ListView):
    model = Quiz
    template_name = 'view_quiz_category.html'

    def dispatch(self, request, *args, **kwargs):
        self.category = get_object_or_404(
            CourseInfo,
            category=self.kwargs['category_name']
        )

        return super(ViewQuizListByCourse, self). \
            dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(ViewQuizListByCourse, self) \
            .get_context_data(**kwargs)

        context['category'] = self.category
        return context

    def get_queryset(self):
        queryset = super(ViewQuizListByCourse, self).get_queryset()
        return queryset.filter(category=self.category, draft=False)


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


class QuizTake(FormView):
    form_class = QuestionForm
    template_name = 'question.html'
    result_template_name = 'result.html'
    single_complete_template_name = 'single_complete.html'

    def dispatch(self, request, *args, **kwargs):
        self.quiz = get_object_or_404(Quiz, url=self.kwargs['quiz_name'])
        if self.quiz.draft and not request.user.has_perm('quiz.change_quiz'):
            raise PermissionDenied

        try:
            self.logged_in_user = self.request.user.is_authenticated()
        except TypeError:
            self.logged_in_user = self.request.user.is_authenticated

        if self.logged_in_user:
            self.sitting = Sitting.objects.user_sitting(request.user, self.quiz)
        else:
            self.sitting = self.anon_load_sitting()

        if self.sitting is False:
            return render(request, self.single_complete_template_name)

        return super(QuizTake, self).dispatch(request, *args, **kwargs)

    def get_form(self, *args, **kwargs):
        if self.logged_in_user:
            self.question = self.sitting.get_first_question()
            self.progress = self.sitting.progress()
        else:
            self.question = self.anon_next_question()
            self.progress = self.anon_sitting_progress()

        if self.question.__class__ is SA_Question:
            form_class = SAForm
        else:
            form_class = self.form_class
        return form_class(**self.get_form_kwargs())

    def get_form_kwargs(self):
        kwargs = super(QuizTake, self).get_form_kwargs()

        return dict(kwargs, question=self.question)

    def form_valid(self, form):
        if self.logged_in_user:
            self.form_valid_user(form)
            if self.sitting.get_first_question() is False:
                return self.final_result_user()
        else:
            self.form_valid_anon(form)
            if not self.request.session[self.quiz.anon_q_list()]:
                return self.final_result_anon()

        self.request.POST = {}

        return super(QuizTake, self).get(self, self.request)

    def get_context_data(self, **kwargs):
        context = super(QuizTake, self).get_context_data(**kwargs)
        context['question'] = self.question
        context['quiz'] = self.quiz
        if hasattr(self, 'previous'):
            context['previous'] = self.previous
        if hasattr(self, 'progress'):
            context['progress'] = self.progress
        return context

    def form_valid_user(self, form):
        progress, c = Progress.objects.get_or_create(user=self.request.user)
        guess = form.cleaned_data['answers']
        is_correct = self.question.check_if_correct(guess)

        if is_correct is True:
            self.sitting.add_to_score(1)
            progress.update_score(self.question, 1, 1)
        else:
            self.sitting.add_incorrect_question(self.question)
            progress.update_score(self.question, 0, 1)

        if self.quiz.answers_at_end is not True:
            self.previous = {'previous_answer': guess,
                             'previous_outcome': is_correct,
                             'previous_question': self.question,
                             'answers': self.question.get_answers(),
                             'question_type': {self.question
                                                   .__class__.__name__: True}}
        else:
            self.previous = {}

        self.sitting.add_user_answer(self.question, guess)
        self.sitting.remove_first_question()

    def final_result_user(self):
        results = {
            'quiz': self.quiz,
            'score': self.sitting.get_current_score,
            'max_score': self.sitting.get_max_score,
            'percent': self.sitting.get_percent_correct,
            'sitting': self.sitting,
            'previous': self.previous,
        }

        self.sitting.mark_quiz_complete()

        if self.quiz.answers_at_end:
            results['questions'] = \
                self.sitting.get_questions(with_answers=True)
            results['incorrect_questions'] = \
                self.sitting.get_incorrect_questions

        if self.quiz.exam_paper is False:
            self.sitting.delete()

        return render(self.request, self.result_template_name, results)

    def anon_load_sitting(self):
        if self.quiz.single_attempt is True:
            return False

        if self.quiz.anon_q_list() in self.request.session:
            return self.request.session[self.quiz.anon_q_list()]
        else:
            return self.new_anon_quiz_session()

    def new_anon_quiz_session(self):
        """
        Sets the session variables when starting a quiz for the first time
        as a non signed-in user
        """
        self.request.session.set_expiry(259200)  # expires after 3 days
        questions = self.quiz.get_questions()
        question_list = [question.id for question in questions]

        if self.quiz.random_order is True:
            random.shuffle(question_list)

        # if self.quiz.max_questions and (self.quiz.max_questions
        #                                 < len(question_list)):
        #     question_list = question_list[:self.quiz.max_questions]

        # session score for anon users
        self.request.session[self.quiz.anon_score_id()] = 0

        # session list of questions
        self.request.session[self.quiz.anon_q_list()] = question_list

        # session list of question order and incorrect questions
        self.request.session[self.quiz.anon_q_data()] = dict(
            incorrect_questions=[],
            order=question_list,
        )

        return self.request.session[self.quiz.anon_q_list()]

    def anon_next_question(self):
        next_question_id = self.request.session[self.quiz.anon_q_list()][0]
        return Question.objects.get_subclass(id=next_question_id)

    def anon_sitting_progress(self):
        total = len(self.request.session[self.quiz.anon_q_data()]['order'])
        answered = total - len(self.request.session[self.quiz.anon_q_list()])
        return (answered, total)

    def form_valid_anon(self, form):
        guess = form.cleaned_data['answers']
        is_correct = self.question.check_if_correct(guess)

        if is_correct:
            self.request.session[self.quiz.anon_score_id()] += 1
            anon_session_score(self.request.session, 1, 1)
        else:
            anon_session_score(self.request.session, 0, 1)
            self.request \
                .session[self.quiz.anon_q_data()]['incorrect_questions'] \
                .append(self.question.id)

        self.previous = {}
        if self.quiz.answers_at_end is not True:
            self.previous = {'previous_answer': guess,
                             'previous_outcome': is_correct,
                             'previous_question': self.question,
                             'answers': self.question.get_answers(),
                             'question_type': {self.question
                                                   .__class__.__name__: True}}

        self.request.session[self.quiz.anon_q_list()] = \
            self.request.session[self.quiz.anon_q_list()][1:]

    def final_result_anon(self):
        score = self.request.session[self.quiz.anon_score_id()]
        q_order = self.request.session[self.quiz.anon_q_data()]['order']
        max_score = len(q_order)
        percent = int(round((float(score) / max_score) * 100))
        session, session_possible = anon_session_score(self.request.session)
        if score is 0:
            score = "0"

        results = {
            'score': score,
            'max_score': max_score,
            'percent': percent,
            'session': session,
            'possible': session_possible
        }

        del self.request.session[self.quiz.anon_q_list()]

        if self.quiz.answers_at_end:
            results['questions'] = sorted(
                self.quiz.question_set.filter(id__in=q_order)
                    .select_subclasses(),
                key=lambda q: q_order.index(q.id))

            results['incorrect_questions'] = (
                self.request
                    .session[self.quiz.anon_q_data()]['incorrect_questions'])

        else:
            results['previous'] = self.previous

        del self.request.session[self.quiz.anon_q_data()]

        return render(self.request, 'result.html', results)


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

from django.http import JsonResponse

class MCQuestionCreateView(AjaxableResponseMixin, CreateView):
    model = MCQuestion
    form_class = MCQuestionForm
    #success_url = reverse_lazy('quiz_create')
    template_name = 'ajax/mcquestion_form_ajax.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs) 
        if self.request.POST:
            context['answers_formset'] = AnsFormset(self.request.POST)
        else:
            context['answers_formset'] = AnsFormset()
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
    success_url = reverse_lazy('quiz_create')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)        
        if self.request.POST:
            context['answers_formset'] = AnsFormset(self.request.POST, instance = self.object)
        else:
            context['answers_formset'] = AnsFormset(instance = self.object)
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

class MCQuestionUpdateFromQuiz(UpdateView):
    model = MCQuestion
    form_class = MCQuestionForm
    success_url = reverse_lazy('quiz_create')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)        
        if self.request.POST:
            context['answers_formset'] = AnsFormset(self.request.POST, instance = self.object)
        else:
            context['answers_formset'] = AnsFormset(instance = self.object)
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


def MCQuestionDeleteView(request, pk):
    MCQuestion.objects.filter(pk=pk).delete()
    return redirect("mcquestion_list")

class MCQuestionCreateFromQuiz(CreateView):
    model = MCQuestion
    fields = ['figure', 'content', 'explanation', 'answer_order']

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
            'quiz_detail',
            kwargs = {'pk' : self.kwargs['quiz_id']},
        )

class MCQuestionUpdateFromQuiz(UpdateView):
    model = MCQuestion
    fields = ['figure', 'content', 'explanation', 'answer_order']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)        
        if self.request.POST:
            context['answers_formset'] = AnsFormset(self.request.POST, instance = self.object)
        else:
            context['answers_formset'] = AnsFormset(instance = self.object)
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
            'quiz_detail',
            kwargs = {'pk' : self.kwargs['quiz_id']},
        )

# -------------------------_Question Views------------------

class TFQuestionListView(ListView):
    model = TF_Question


class TFQuestionCreateView(AjaxableResponseMixin, CreateView):
    model = TF_Question
    form_class = TFQuestionForm
    #success_url = reverse_lazy('quiz_create')
    template_name = 'ajax/tfquestion_form_ajax.html'

    def form_valid(self, form):
        vform = super().form_valid(form)
        new_tfq = {}
        new_tfq['new_tfq_id'] = self.object.id
        new_tfq['new_tfq_content'] = self.object.content
        return JsonResponse(new_tfq)

class TFQuestionCreateFromQuiz(CreateView):
    model = TF_Question
    fields = ['figure', 'content', 'explanation', 'correct']
    
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
            'quiz_detail',
            kwargs = {'pk' : self.kwargs['quiz_id']},
        )

class TFQuestionUpdateFromQuiz(UpdateView):
    model = TF_Question
    fields = ['figure', 'content', 'explanation', 'correct']
    
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
            'quiz_detail',
            kwargs = {'pk' : self.kwargs['quiz_id']},
        )


class TFQuestionUpdateView(UpdateView):
    model = TF_Question
    form_class = TFQuestionForm
    success_url = reverse_lazy('quiz_create')


class TFQuestionDetailView(DetailView):
    model = TF_Question


def TFQuestionDeleteView(request, pk):
    TF_Question.objects.filter(pk=pk).delete()
    return redirect("tfquestion_list")

# ------------------------- SA_Question Views------------------

class SAQuestionListView(ListView):
    model = SA_Question

class SAQuestionCreateView(AjaxableResponseMixin, CreateView):
    model = SA_Question
    form_class = SAQuestionForm
    #success_url = reverse_lazy('quiz_create')
    template_name = 'ajax/saquestion_form_ajax.html'

    def form_valid(self, form):
        vform = super().form_valid(form)
        new_saq = {}
        new_saq['new_saq_id'] = self.object.id
        new_saq['new_Saq_content'] = self.object.content
        return JsonResponse(new_saq)

class SAQuestionCreateFromQuiz(CreateView):
    model = SA_Question
    fields = ['figure', 'content', 'explanation']
    
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
            'quiz_detail',
            kwargs = {'pk' : self.kwargs['quiz_id']},
        )

class SAQuestionUpdateFromQuiz(UpdateView):
    model = SA_Question
    fields = ['figure', 'content', 'explanation']
    
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
            'quiz_detail',
            kwargs = {'pk' : self.kwargs['quiz_id']},
        )

class SAQuestionUpdateView(UpdateView):
    model = SA_Question
    form_class = SAQuestionForm
    success_url = reverse_lazy('quiz_create')

class SAQuestionDetailView(DetailView):
    model = SA_Question

def SAQuestionDeleteView(request, pk):
    SA_Question.objects.filter(pk=pk).delete()
    return redirect("essayquestion_list")
