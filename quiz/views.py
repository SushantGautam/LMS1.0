import json
import random

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.db import transaction
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import DetailView, ListView, TemplateView, FormView, CreateView, UpdateView
from django_addanother.views import CreatePopupMixin

from LMS.auth_views import QuizInfoAuthMxnCls, QuizInfoAuth, AdminAuthMxnCls, StudentCourseAuth
from WebApp.models import CourseInfo, ChapterInfo, InningGroup, InningInfo
from .forms import QuestionForm, SAForm, QuizForm, TFQuestionForm, SAQuestionForm, MCQuestionForm, AnsFormset, \
    QuizBasicInfoForm, QuestionQuizForm, ChooseMCQForm, ChooseSAQForm, ChooseTFQForm, MCForm, TFForm
from .models import Quiz, Progress, Sitting, MCQuestion, TF_Question, Question, SA_Question


class QuizMarkerMixin(object):
    @method_decorator(login_required)
    # @method_decorator(permission_required('quiz.view_sittings'))
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
    # template_name = 'quiz/test_temp.html'
    model = Quiz
    # fields = ['title']
    form_class = QuizForm
    success_url = reverse_lazy('quiz_list')


class QuizListView(AdminAuthMxnCls, ListView):
    model = Quiz

    def get_queryset(self):
        queryset = super(QuizListView, self).get_queryset().order_by('-pk')
        print(queryset.values('pk', 'title'))
        return queryset.filter(cent_code=self.request.user.Center_Code)


class QuizUpdateView(AdminAuthMxnCls, QuizInfoAuthMxnCls, UpdateView):
    model = Quiz
    form_class = QuizForm


class QuizDetailView(AdminAuthMxnCls, QuizInfoAuthMxnCls, DetailView):
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
    messages.add_message(request, messages.SUCCESS,
                         'Quiz Deleted Successfully.')
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
            .filter(complete=True, user__Center_Code=self.request.user.Center_Code)

        user_filter = self.request.GET.get('user_filter')
        if user_filter:
            queryset = queryset.filter(user__username__icontains=user_filter)

        return queryset


class QuizMarkingDetail(QuizMarkerMixin, DetailView):
    model = Sitting

    def post(self, request, *args, **kwargs):
        sitting = self.get_object()

        q_to_toggle = request.POST.get('saq_id', None)
        if q_to_toggle:
            q = Question.objects.get_subclass(id=int(q_to_toggle))
            indx = [int(n) for n in sitting.question_order.split(',') if n].index(q.id)
            print(request.POST['new_score'], "new_score")
            print(indx, "index")
            ssl = sitting.score_list
            if not ssl:
                ssl = ''
            score_list = [s for s in ssl.split(',') if s]
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
            score = [s for s in context['sitting'].score_list.split(',') if s][i]
            q.score_obtained = score
            total += q.score
            if score != "not_graded":
                total_score_obtained += float(score)
        context['total_score_obtained'] = total_score_obtained
        context['total'] = total

        return context


class QuizTake(FormView):
    form_class = QuestionForm
    template_name = 'question.html'
    result_template_name = 'result.html'
    single_complete_template_name = 'single_complete.html'
    current_question_number = 0

    def dispatch(self, request, *args, **kwargs):
        self.quiz = get_object_or_404(Quiz, url=self.kwargs['quiz_name'])
        self.current_question_number = self.request.GET.get('q') if self.request.GET.get('q') else 0
        if QuizInfoAuth(request, self.quiz.pk) != 1:  # check if quiz belongs to the same center as user
            return redirect('login')
        if StudentCourseAuth(request,
                             self.quiz.course_code.pk) != 1:  # check if student has access to course that the quiz belongs to
            return redirect('login')
        if self.quiz.draft and not request.user.has_perm('quiz.change_quiz'):
            raise PermissionDenied

        try:
            self.logged_in_user = self.request.user.is_authenticated()
        except TypeError:
            self.logged_in_user = self.request.user.is_authenticated

        if self.logged_in_user:
            self.sitting = Sitting.objects.user_sitting(
                request.user, self.quiz)
        else:
            self.sitting = self.anon_load_sitting()

        if self.sitting is False:
            messages.add_message(request, messages.ERROR,
                                 'You have already sat this exam and only one sitting is permitted')
            # return render(request, self.single_complete_template_name)
            sittingObj = Sitting.objects.filter(user=self.request.user,
                                                quiz__pk=self.quiz.pk,
                                                complete=True).last()
            return redirect('student_progress_detail', pk=sittingObj.id)

        return super(QuizTake, self).dispatch(request, *args, **kwargs)

    def get_form(self, *args, **kwargs):
        if self.logged_in_user:
            question = None
            # if query parameter is present, then fetch the form of the question.
            if self.current_question_number:
                question = int(self.current_question_number)
            self.question = self.sitting.get_first_question(question_index=question)
            self.progress = self.sitting.progress()
        else:
            self.question = self.anon_next_question()
            self.progress = self.anon_sitting_progress()

        if self.question.__class__ is SA_Question:
            form_class = SAForm
        elif self.question.__class__ is MCQuestion:
            form_class = MCForm
        else:
            # form_class = self.form_class
            form_class = TFForm
        return form_class(**self.get_form_kwargs())

    def get_form_kwargs(self):
        kwargs = super(QuizTake, self).get_form_kwargs()

        # if answer is already submitted. Fetch the answer and initialize the form answer
        answer = None
        if self.request.GET.get('q'):
            # if sitting is available and answer is present in "user_answer" dict in sitting model, then fetch the answer.
            if self.sitting and len(json.loads(self.sitting.user_answers).keys()) > 0 and str(
                    self.question.pk) in json.loads(self.sitting.user_answers):
                answer = json.loads(self.sitting.user_answers)[str(self.question.pk)]
        return dict(kwargs, question=self.question, answer=answer)

    def form_valid(self, form):
        if self.logged_in_user:
            self.form_valid_user(form)
            if self.sitting.get_first_question() is False or self.sitting.complete:
                return self.final_result_user()
        else:
            self.form_valid_anon(form)
            if not self.request.session[self.quiz.anon_q_list()]:
                return self.final_result_anon()

        self.request.POST = {}
        if len(self.sitting.question_order.split(',')) <= int(self.current_question_number):
            self.request.GET = {}
            self.current_question_number = None
        else:
            if self.sitting.question_order.split(',')[int(self.current_question_number)] == '':
                self.request.GET = {}
                self.current_question_number = None
            else:
                self.request.method = "GET"
                self.request.GET = {'q': str(int(self.current_question_number) + 1)}
                self.current_question_number = str(int(self.current_question_number) + 1)
        return super(QuizTake, self).get(self, self.request)

    def get_context_data(self, **kwargs):
        context = super(QuizTake, self).get_context_data(**kwargs)
        context['question'] = self.question
        context['quiz'] = self.quiz
        context['sitting_id'] = self.sitting.id
        context['sitting'] = self.sitting
        if self.sitting.remaining_time == 0:
            context['remaining_time'] = self.quiz.duration
        else:
            context['remaining_time'] = self.sitting.remaining_time
        # context['remaininig_time'] = self.quiz.duration - self.sitting.time_elapsed
        if hasattr(self, 'previous'):
            context['previous'] = self.previous
        if hasattr(self, 'progress'):
            context['progress'] = self.progress

        # get current question number from question_order list.
        # since list index starts from 0, add 1 for question number.
        context['question_number'] = int(self.sitting.question_order.split(',').index(str(self.question.pk))) + 1
        # check if question has previous/next question or not for button.
        context['has_previous'] = True
        context['has_next'] = True
        # if list index of question is 0, then this is first question, therefore there cannot be previous
        if int(self.sitting.question_order.split(',').index(str(self.question.pk))) == 0:
            context['has_previous'] = False
        # if question is to be attempted for first time, then assumption is all following questions after current is not taken, hence no next.
        if str(self.question.id) in self.sitting.question_list.split(','):
            context['has_next'] = False

        return context

    def form_valid_user(self, form):
        progress, c = Progress.objects.get_or_create(user=self.request.user)
        # if type(self.question) is TF_Question:
        #     guess = form.cleaned_data['answers'][0]        # because saq and mcq share same form
        # else:                                              # so for tfq, need to remove list '[]'                     
        #     guess = form.cleaned_data['answers']
        guess = form.cleaned_data['answers']
        print("multiple selected values: ", guess)

        ssl = self.sitting.score_list
        if not ssl:
            ssl = ''
        score_list = [s for s in ssl.split(',') if s]
        score = self.question.score

        if type(self.question) is MCQuestion:
            num_correct_options = self.question.get_num_correct_options()  # get number of correct options
            num_options = self.question.get_answers().count()
            per_score = self.question.score / num_correct_options
            score = 0
            is_correct = True

            ##############################################################
            ##### loop for all user chosen:                           ####
            ##### chosen - 1; correct - 1 => +score                   ####
            ##### chosen - 1; correct - 0 => -score * negative_factor ####
            ##### chosen - 0; correct - 1 => 0                        ####
            ##### chosen - 0; correct - 0 => 0                        ####
            ##### so we only care about chosen values                 ####
            ##############################################################

            for g in guess:
                if self.question.check_if_correct(g):
                    score += per_score
                else:
                    is_correct = False  ###### user selected wrong answer
                    if self.sitting.quiz.negative_marking:
                        score -= float(per_score * self.sitting.quiz.negative_percentage) / 100.0
                    else:
                        score += 0

            num_correct_guess = sum([self.question.check_if_correct(g) for g in guess])
            # score = per_score * num_correct_guess
            # incorrect_score = per_score * (num_correct_options - num_correct_guess)
            if not (num_correct_options == num_correct_guess):
                is_correct = False  ####### user didn't select all answers
        else:
            is_correct = self.question.check_if_correct(guess)

        if is_correct is True:
            if type(self.question) is SA_Question:
                if str(self.question.id) in self.sitting.question_list.split(','):
                    score = 'not_graded'
                    self.sitting.add_to_score(0)
                    progress.update_score(self.question, 0, 1)
                    score_list.append(str(score))
            else:
                if str(self.question.id) in self.sitting.question_list.split(','):
                    self.sitting.add_to_score(score)
                    progress.update_score(self.question, score, score)
                    score_list.append(str(score))
                else:
                    current_score_list = self.sitting.score_list.split(',')
                    current_incorrect_list = self.sitting.incorrect_questions.split(',')
                    # update score for T/F question and MCQ. Since the score is not graded for SAQ while taking quiz, update score on SAQ is not necessary
                    for idx, value in enumerate(current_score_list):
                        if idx == int(self.sitting.question_order.split(',').index(str(self.question.pk))):
                            prev_score = current_score_list[idx]
                            # self.sitting.add_to_score(-prev_score)
                            # deduct previous score and add new score
                            self.sitting.add_to_score((-float(prev_score) + float(score)))
                            progress.update_score(self.question, (-float(prev_score) + float(score)),
                                                  -(float(prev_score) + float(score)))
                            score_list[idx] = (str(score))

                            # remove from incorrect list
                            if str(self.question.pk) in current_incorrect_list:
                                current_incorrect_list.remove(str(self.question.pk))
                                self.sitting.incorrect_questions = ','.join(current_incorrect_list)

        else:
            if str(self.question.id) in self.sitting.question_list.split(','):
                self.sitting.add_incorrect_question(self.question)
            else:
                current_incorrect_list = self.sitting.incorrect_questions.split(',')
                for idx, value in enumerate(current_incorrect_list):
                    if str(self.question.pk) not in current_incorrect_list:
                        self.sitting.add_incorrect_question(self.question)
                    else:
                        if idx == int(self.sitting.incorrect_questions.split(',').index(str(self.question.pk))):
                            current_incorrect_list[idx] = (str(self.question.pk))
                            self.sitting.incorrect_questions = ','.join(current_incorrect_list)

            if type(self.question) is MCQuestion:
                negative_score = score
            elif self.sitting.quiz.negative_marking:
                negative_score = -(float(self.sitting.quiz.negative_percentage * score) / 100)
            else:
                negative_score = 0

            if str(self.question.id) in self.sitting.question_list.split(','):
                self.sitting.add_to_score(negative_score)
                progress.update_score(self.question, negative_score, score)
                score_list.append(str(negative_score))
            else:
                current_score_list = self.sitting.score_list.split(',')
                # same as the correct score.
                for idx, value in enumerate(current_score_list):
                    if idx == int(self.sitting.question_order.split(',').index(str(self.question.pk))):
                        prev_score = current_score_list[idx]
                        # self.sitting.add_to_score(-prev_score)
                        # deduct previous score and add new score
                        self.sitting.add_to_score((-float(prev_score) + float(negative_score)))
                        progress.update_score(self.question, (-float(prev_score) + float(negative_score)),
                                              (-float(prev_score) + float(score)))
                        score_list[idx] = (str(negative_score))

        self.sitting.score_list = ','.join(score_list)

        # if self.quiz.answers_at_end is not True:
        #     self.previous = {'previous_answer': guess,
        #                      'previous_outcome': is_correct,
        #                      'previous_question': self.question,
        #                      'answers': self.question.get_answers(),
        #                      'question_type': {self.question
        #                                            .__class__.__name__: True}}
        # else:
        #     self.previous = {}

        self.previous = {}

        self.sitting.add_user_answer(self.question, guess)
        # if question is in question_list, then only remove the question.
        # In case of answer update, question is already removed. Therefore, no need if previously attempted
        if str(self.question.id) in self.sitting.question_list.split(','):
            self.sitting.remove_first_question(question_id=str(self.question.id)) if self.request.GET.get(
                'q') else self.sitting.remove_first_question()

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

        # if self.quiz.exam_paper is False:
        #    self.sitting.delete()
        if self.request.GET.get('iframe'):
            return redirect(
                reverse('student_progress_detail', kwargs={'pk': self.sitting.id}) + '?iframe=' + self.request.GET.get(
                    'iframe'))
        else:
            return redirect('student_progress_detail', pk=self.sitting.id)

        # return render(self.request, self.result_template_name, results)

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
        print("get qns:")
        print(questions)
        print("qn list:")
        print(question_list)

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


def UpdateQuizTime(request):
    if request.method == 'POST':
        quiz = Quiz.objects.get(pk=request.POST.get('quiz_id'))
        if quiz.exam_paper:
            sitting = Sitting.objects.get(pk=request.POST.get('sitting_id'))
            remaining_time = request.POST.get('remaining_time')
            sitting.remaining_time = remaining_time
            if int(remaining_time) < 1:
                sitting.end = timezone.now()
                sitting.complete = True
            sitting.save()

            if request.GET.get('iframe'):
                url = "/students/quiz/progress/" + str(sitting.id) + "/?iframe=" + request.GET.get('iframe')
            else:
                url = "/students/quiz/progress/" + str(sitting.id)

            return JsonResponse({
                'sitting_remaining_time': sitting.remaining_time,
                'url': url if sitting.complete else 0
            }, status=200)
        return JsonResponse({
            'error_message': 'Only for exams',
        }, status=500)


class QuestionCreateView(CreateView):
    model = Question
    form_class = QuestionForm


# ------------------------- MC_Question Views------------------


class MCQuestionListView(ListView):
    model = MCQuestion


class MCQuestionCreateView(AjaxableResponseMixin, CreateView):
    model = MCQuestion
    form_class = MCQuestionForm
    # success_url = reverse_lazy('quiz_create')
    template_name = 'ajax_quiz/mcquestion_form_ajax.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['answers_formset'] = AnsFormset(self.request.POST),
            context['quiz_id'] = self.request.POST.get("quiz_id", None)
        else:
            context['answers_formset'] = AnsFormset()
            context['course_from_quiz'] = self.request.GET["course_from_quiz"]
            context['quiz_id'] = self.request.GET.get("quiz_id", None)
            context['post_url'] = reverse('mcquestion_create')
        return context

    def form_valid(self, form):
        vform = super().form_valid(form)
        context = self.get_context_data()
        ans = context['answers_formset'][0]
        if context['quiz_id'] is not None:
            get_object_or_404(Quiz, id=context['quiz_id']).mcquestion.add(self.object)
        with transaction.atomic():
            for f in ans:
                print("is changed: ", f.has_changed())
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

    template_name = 'ajax_quiz/mcquestion_form_ajax.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['answers_formset'] = AnsFormset(
                self.request.POST, instance=self.object)
        else:
            ansFormSet = AnsFormset(instance=self.object)
            ansFormSet.extra = 0  # extra field on edit is removed
            context['answers_formset'] = ansFormSet
            context['post_url'] = reverse('mcquestion_update', kwargs={'pk': self.object.pk})
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


class TFQuestionListView(ListView):
    model = TF_Question


class TFQuestionCreateView(AjaxableResponseMixin, CreateView):
    model = TF_Question
    form_class = TFQuestionForm
    template_name = 'ajax_quiz/tfquestion_form_ajax.html'

    def form_valid(self, form):
        vform = super().form_valid(form)
        new_tfq = {}
        new_tfq['new_tfq_id'] = self.object.id
        new_tfq['new_tfq_content'] = self.object.content
        context = self.get_context_data()
        if context['quiz_id'] is not None:
            get_object_or_404(Quiz, id=context['quiz_id']).tfquestion.add(self.object)
        return JsonResponse(new_tfq)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['quiz_id'] = self.request.POST.get("quiz_id", None)
        else:
            context['course_from_quiz'] = self.request.GET["course_from_quiz"]
            context['quiz_id'] = self.request.GET.get("quiz_id", None)
            context['post_url'] = reverse('tfquestion_create')
        return context


class TFQuestionUpdateView(UpdateView):
    model = TF_Question
    form_class = TFQuestionForm
    template_name = 'ajax_quiz/tfquestion_form_ajax.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.GET:
            context['course_from_quiz'] = self.request.GET["course_from_quiz"]
            context['post_url'] = reverse('tfquestion_update', kwargs={'pk': self.object.pk})
        return context


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
    # success_url = reverse_lazy('quiz_create')
    template_name = 'ajax_quiz/saquestion_form_ajax.html'

    def form_valid(self, form):
        vform = super().form_valid(form)
        new_saq = {}
        new_saq['new_saq_id'] = self.object.id
        new_saq['new_saq_content'] = self.object.content
        context = self.get_context_data()
        if context['quiz_id'] is not None:
            get_object_or_404(Quiz, id=context['quiz_id']).saquestion.add(self.object)
        return JsonResponse(new_saq)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['quiz_id'] = self.request.POST.get("quiz_id", None)
        else:
            context['course_from_quiz'] = self.request.GET["course_from_quiz"]
            context['quiz_id'] = self.request.GET.get("quiz_id", None)
            context['post_url'] = reverse('saquestion_create')
        return context


class SAQuestionUpdateView(UpdateView):
    model = SA_Question
    form_class = SAQuestionForm
    template_name = 'ajax_quiz/saquestion_form_ajax.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.GET:
            context['course_from_quiz'] = self.request.GET["course_from_quiz"]
            context['post_url'] = reverse('saquestion_update', kwargs={'pk': self.object.pk})
        return context


class SAQuestionDetailView(DetailView):
    model = SA_Question


def SAQuestionDeleteView(request, pk):
    SA_Question.objects.filter(pk=pk).delete()
    return redirect("essayquestion_list")


from formtools.wizard.views import SessionWizardView
from .forms import QuizForm1, QuizForm2, QuizForm3

FORMS = [("form1", QuizForm1),
         ("form2", QuizForm2),
         ("form3", QuizForm3)]

TEMPLATES = {"form1": "wizard/step1.html",
             "form2": "wizard/step2.html",
             "form3": "wizard/step3.html"}
TEACHER_TEMPLATES = {"form1": "teacher_quiz/step1.html",
                     "form2": "teacher_quiz/step2.html",
                     "form3": "teacher_quiz/step3.html"}


class QuizCreateWizard(SessionWizardView):
    form_list = FORMS

    def get_template_names(self):
        if '/teachers' in self.request.path:
            return [TEACHER_TEMPLATES[self.steps.current]]
        else:
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
        # my_quiz.url = urllib.parse.quote_plus(str(my_quiz.title) + str(my_quiz.id))
        my_quiz.url = 'quiz' + str(my_quiz.id)
        my_quiz.cent_code = self.request.user.Center_Code
        my_quiz.save()
        print("MCQ's: ", MCQuestion.objects.filter(pk__in=mcq).values_list("content"))
        my_quiz.mcquestion.add(*mcq)
        my_quiz.tfquestion.add(*tfq)
        my_quiz.saquestion.add(*saq)
        # if self.request.user.Is_Teacher and not self.request.user.Is_CenterAdmin:
        if '/teachers' in self.request.path:
            return redirect('teacher_quiz_list')
        else:
            return redirect('quiz_list')

    def get_form_kwargs(self, step):
        return_dict = {}
        if step == 'form3':
            step1_data = self.get_cleaned_data_for_step('form1')
            mc_queryset = MCQuestion.objects.filter(course_code=step1_data['course_code'])
            tf_queryset = TF_Question.objects.filter(course_code=step1_data['course_code'])
            sa_queryset = SA_Question.objects.filter(course_code=step1_data['course_code'])

            return_dict['mc_queryset'] = mc_queryset
            return_dict['sa_queryset'] = sa_queryset
            return_dict['tf_queryset'] = tf_queryset
        return return_dict

    def get_form(self, step=None, data=None, files=None):
        form = super().get_form(step, data, files)

        # determine the step if not given
        if step is None:
            step = self.steps.current

        if step == 'form1':
            if '/teachers' in self.request.path:
                form.fields["course_code"].queryset = CourseInfo.objects.filter(
                    pk__in=[id.pk for id in self.request.user.get_teacher_courses()['courses']])
            else:
                form.fields["course_code"].queryset = CourseInfo.objects.filter(
                    Center_Code=self.request.user.Center_Code)

        if step == 'form2':
            step1_data = self.get_cleaned_data_for_step('form1')
            step1_course = step1_data['course_code']
            form.fields["chapter_code"].queryset = ChapterInfo.objects.filter(Course_Code=step1_course)

        if step == 'form3':
            # step1_data = self.get_cleaned_data_for_step('form1')
            # mc_queryset = MCQuestion.objects.filter(course_code=step1_data['course_code'])
            # tf_queryset = TF_Question.objects.filter(course_code=step1_data['course_code'])
            # sa_queryset = SA_Question.objects.filter(course_code=step1_data['course_code'])
            print("form media: ", form.media)

        return form

    def get_context_data(self, form, **kwargs):
        context = super().get_context_data(form=form, **kwargs)
        if self.steps.current == 'form3':
            step1_data = self.get_cleaned_data_for_step('form1')
            step1_course = step1_data['course_code']
            context.update({'course_from_quiz': step1_course})
        return context


class CreateQuizAjax(CreateView):
    model = Quiz
    form_class = QuizForm
    template_name = 'ajax_quiz/quiz_create_chapter_ajax.html'

    def form_valid(self, form):
        context = self.get_context_data()
        if form.is_valid():
            print("form valid")
            print(form)
            self.object = form.save(commit=False)
            self.object.cent_code = self.request.user.Center_Code
            course_id = self.request.GET.get("course_id", None)
            course_id = None if course_id == 'None' else int(course_id)
            chapter_id = self.request.GET.get("chapter_id", None)
            chapter_id = None if chapter_id == 'None' else int(chapter_id)
            if course_id:
                self.object.course_code = CourseInfo.objects.get(id=course_id)
            if chapter_id:
                self.object.chapter_code = ChapterInfo.objects.get(id=chapter_id)
            self.object.pre_test = True if self.request.GET.get("test_type", None) == 'pre_test' else False
            self.object.post_test = True if self.request.GET.get("test_type", None) == 'post_test' else False
            self.object.exam_paper = True if self.request.GET.get("test_type", None) == 'exam_paper' else False
            # self.object.single_attempt = True if self.request.GET.get("test_type", None) == 'exam_paper' else False
            self.object.save()
        self.object.url = 'quiz' + str(self.object.id)
        super().form_valid(form)
        response = {'url': self.request.build_absolute_uri(reverse('quiz_detail', kwargs={'pk': self.object.id})),
                    'quiz_id': self.object.id,
                    'teacher_url': self.request.build_absolute_uri(
                        reverse('teacher_quiz_detail', kwargs={'pk': self.object.id})),
                    'student_url': self.request.build_absolute_uri(
                        reverse('quiz_question', kwargs={'quiz_name': self.object.url}))}
        return JsonResponse(response)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['chapter_pk'] = self.request.GET.get("chapter_id", None)
        context['course_id'] = self.request.GET.get("course_id", None)
        context['test_type'] = self.request.GET.get("test_type", None)
        return context

    def get_success_url(self):
        context = self.get_context_data()
        if context['test_type'] == "exam_paper":
            return reverse(
                'courseinfo_detail',
                kwargs={
                    'pk': context['course_id'],
                },
            )
        else:
            return reverse(
                'chapterinfo_detail',
                kwargs={
                    'course': context['course_id'],
                    'pk': context['chapter_pk'],
                },
            )

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({'course_id': self.request.GET.get("course_id", None)})
        return kwargs


class UpdateQuizBasicInfo(AdminAuthMxnCls, QuizInfoAuthMxnCls, UpdateView):
    model = Quiz
    form_class = QuizBasicInfoForm
    template_name = 'quiz/quiz_update_basic_info.html'

    def get_form_kwargs(self):
        default_kwargs = super().get_form_kwargs()
        default_kwargs['current_obj'] = self.object
        return default_kwargs

    def get_success_url(self):
        return reverse(
            'quiz_detail',
            kwargs={'pk': self.object.pk},
        )


class GetCourseChapter(View):
    def get(self, request):
        my_course = CourseInfo.objects.get(id=request.GET['course_id'])
        resp = {}
        for my_dict in my_course.chapterinfos.all().values('id', 'Chapter_Name'):
            resp[my_dict['id']] = my_dict['Chapter_Name']
        print(resp)
        return JsonResponse(resp)


class RemoveMcqLink(View):
    def post(self, request, **kwargs):
        my_obj = get_object_or_404(Quiz, id=self.kwargs['quiz_id'])
        if my_obj.question_count() > 1:
            my_obj.mcquestion.remove(get_object_or_404(MCQuestion, id=self.kwargs['qn_id']))
        else:
            messages.add_message(request, messages.ERROR,
                                 'At least one question must be available in quiz.')
        return HttpResponseRedirect(
            reverse(
                'quiz_detail',
                kwargs={'pk': my_obj.pk},
            )
        )


class RemoveTfqLink(View):
    def post(self, request, **kwargs):
        my_obj = get_object_or_404(Quiz, id=self.kwargs['quiz_id'])
        if my_obj.question_count() > 1:
            my_obj.tfquestion.remove(get_object_or_404(TF_Question, id=self.kwargs['qn_id']))
        else:
            messages.add_message(request, messages.ERROR,
                                 'At least one question must be available in quiz.')
        return HttpResponseRedirect(
            reverse(
                'quiz_detail',
                kwargs={'pk': my_obj.pk},
            )
        )


class RemoveSaqLink(View):
    def post(self, request, **kwargs):
        my_obj = get_object_or_404(Quiz, id=self.kwargs['quiz_id'])
        if my_obj.question_count() > 1:
            my_obj.saquestion.remove(get_object_or_404(SA_Question, id=self.kwargs['qn_id']))
        else:
            messages.add_message(request, messages.ERROR,
                                 'At least one question must be available in quiz.')
        return HttpResponseRedirect(
            reverse(
                'quiz_detail',
                kwargs={'pk': my_obj.pk},
            )
        )


class ActivateQuiz(View):
    def post(self, request, **kwargs):
        my_quiz = get_object_or_404(Quiz, pk=self.kwargs['pk'])
        my_quiz.draft = False
        my_quiz.save()
        redirectUrl = self.request.POST.get('redirect-url')
        if 'teachers' in redirectUrl and 'detail' in redirectUrl:
            return HttpResponseRedirect(
                reverse(
                    'teacher_quiz_detail',
                    kwargs={'pk': self.kwargs['pk']},
                )
            )
        elif 'teachers' in redirectUrl:
            return HttpResponseRedirect(
                reverse(
                    'teacher_quiz_exam_list'
                )
            )
        elif 'detail' in redirectUrl:
            return HttpResponseRedirect(
                reverse(
                    'quiz_detail',
                    kwargs={'pk': self.kwargs['pk']},
                )
            )
        else:
            return HttpResponseRedirect(
                reverse(
                    'quiz_exam_list'
                )
            )


class DeactivateQuiz(View):
    def post(self, request, **kwargs):
        my_quiz = get_object_or_404(Quiz, pk=self.kwargs['pk'])
        my_quiz.draft = True
        my_quiz.save()
        redirectUrl = self.request.POST.get('redirect-url')
        if 'teachers' in redirectUrl and 'detail' in redirectUrl:
            return HttpResponseRedirect(
                reverse(
                    'teacher_quiz_detail',
                    kwargs={'pk': self.kwargs['pk']},
                )
            )
        elif 'teachers' in redirectUrl:
            return HttpResponseRedirect(
                reverse(
                    'teacher_quiz_exam_list'
                )
            )
        elif 'detail' in redirectUrl:
            return HttpResponseRedirect(
                reverse(
                    'quiz_detail',
                    kwargs={'pk': self.kwargs['pk']},
                )
            )
        else:
            return HttpResponseRedirect(
                reverse(
                    'quiz_exam_list'
                )
            )


class QuizExamListView(ListView):
    model = Quiz

    def get_template_names(self):
        if 'teachers' in self.request.path:
            return ['teacher_quiz/exam_list.html']
        elif 'students' in self.request.path:
            return ['student_quiz/exam_list.html']
        else:
            return ['quiz/exam_list.html']

    def get_queryset(self):
        quiz_qs = Quiz.objects.filter(cent_code=self.request.user.Center_Code.id, exam_paper=True)
        innings_Course_Code = InningGroup.objects.filter(Teacher_Code=self.request.user.id).values('Course_Code')
        student_group = self.request.user.groupmapping_set.all()
        active_student_session = InningInfo.objects.filter(Groups__in=student_group, End_Date__gt=timezone.now())
        student_course = InningGroup.objects.filter(inninginfo__in=active_student_session).values("Course_Code")
        if 'teachers' in self.request.path:
            return quiz_qs.filter(course_code__in=innings_Course_Code)
        elif 'students' in self.request.path:
            return quiz_qs.filter(course_code__in=student_course, draft=False)
        else:
            return quiz_qs

    def get_context_data(self, **kwargs):
        old_context = super().get_context_data(**kwargs)
        if 'students' in self.request.path:
            my_sittings = Sitting.objects.filter(user=self.request.user.id, complete=True)
            for x in old_context['object_list']:
                if len(my_sittings.filter(quiz=x.id)) > 0:
                    x.already_submitted = True
                else:
                    x.already_submitted = False

        return old_context


class UpdateQuestions(UpdateView):
    model = Quiz
    form_class = QuestionQuizForm
    template_name = 'quiz/updata_all_questions.html'

    def get_success_url(self):
        return reverse(
            'quiz_detail',
            kwargs={'pk': self.kwargs['pk']},
        )

    def get_form_kwargs(self):
        old_kwargs = super().get_form_kwargs()
        old_kwargs['course_id'] = get_object_or_404(Quiz, pk=self.kwargs['pk']).course_code.id
        return old_kwargs

    def get_context_data(self, **kwargs):
        old_context = super().get_context_data(**kwargs)
        old_context['course_from_quiz'] = get_object_or_404(Quiz, pk=self.kwargs['pk']).course_code
        return old_context


class QuizMCQChoosePrevious(AjaxableResponseMixin, UpdateView):
    model = Quiz
    form_class = ChooseMCQForm
    template_name = 'ajax_quiz/mcquestion_choose_ajax.html'

    def get_form_kwargs(self):
        my_kwargs = super().get_form_kwargs()
        my_kwargs['current_obj'] = get_object_or_404(Quiz, pk=self.kwargs['pk'])
        return my_kwargs

    def get_success_url(self):
        return reverse(
            'quiz_detail',
            kwargs={'pk': self.kwargs['pk']},
        )


class QuizTFQChoosePrevious(AjaxableResponseMixin, UpdateView):
    model = Quiz
    form_class = ChooseTFQForm
    template_name = 'ajax_quiz/tfquestion_choose_ajax.html'

    def get_form_kwargs(self):
        my_kwargs = super().get_form_kwargs()
        my_kwargs['current_obj'] = get_object_or_404(Quiz, pk=self.kwargs['pk'])
        return my_kwargs

    def get_success_url(self):
        return reverse(
            'quiz_detail',
            kwargs={'pk': self.kwargs['pk']},
        )


class QuizSAQChoosePrevious(AjaxableResponseMixin, UpdateView):
    model = Quiz
    form_class = ChooseSAQForm
    template_name = 'ajax_quiz/saquestion_choose_ajax.html'

    def get_form_kwargs(self):
        my_kwargs = super().get_form_kwargs()
        my_kwargs['current_obj'] = get_object_or_404(Quiz, pk=self.kwargs['pk'])
        return my_kwargs

    def get_success_url(self):
        return reverse(
            'quiz_detail',
            kwargs={'pk': self.kwargs['pk']},
        )


def FilterMarkingForTeachers(request, Quiz_Id):
    if QuizInfoAuth(request, Quiz_Id) != 1:  # if Quiz do not belong to the user center then redirect
        return redirect('login')
    filtered = Sitting.objects.filter(user__Center_Code=request.user.Center_Code, quiz=Quiz_Id)
    quiz = Quiz.objects.get(id=Quiz_Id)

    return render(request, 'quiz/sitting_filter.html', {'sitting_list': filtered, 'quiz': quiz})


def DeleteAllSittingAftermarkingfilter(request, Quiz_Id):
    filtered = Sitting.objects.filter(user__Center_Code=request.user.Center_Code, quiz=Quiz_Id).delete()
    messages.add_message(request, messages.SUCCESS,
                         'All Quizzes Deleted Successfully.')

    return redirect('markingfilter', Quiz_Id=Quiz_Id)
