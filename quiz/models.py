from __future__ import unicode_literals

import json
import re

from django.conf import settings
from django.core.exceptions import ValidationError, ImproperlyConfigured
from django.core.validators import (
    MaxValueValidator, validate_comma_separated_integer_list,
)
from django.db import models
from django.urls import reverse
from django.utils.encoding import python_2_unicode_compatible
from django.utils.timezone import now
from django.utils.translation import ugettext_lazy as _
from model_utils.managers import InheritanceManager

from WebApp.models import CourseInfo, ChapterInfo, CenterInfo

# multichoice modelss___________________________________________________________

ANSWER_ORDER_OPTIONS = (
    ('content', _('Content')),
    ('random', _('Random')),
    ('none', _('None'))
)


# class CategoryManager(models.Manager):
#
#     def new_category(self, category):
#         new_category = self.create(category=re.sub('\s+', '-', category)
#                                    .lower())
#
#         new_category.save()
#         return new_category


# @python_2_unicode_compatible
# class Category(models.Model):
#     category = models.CharField(
#         verbose_name=_("Category"),
#         max_length=250, blank=True,
#         unique=True, null=True)
#
#     objects = CategoryManager()
#
#     class Meta:
#         verbose_name = _("Category")
#         verbose_name_plural = _("Categories")
#
#     def __str__(self):
#         return self.category


@python_2_unicode_compatible
# class SubCategory(models.Model):
#     sub_category = models.CharField(
#         verbose_name=_("Sub-Category"),
#         max_length=250, blank=True, null=True)
#
#     category = models.ForeignKey(
#         Category, null=True, blank=True,
#         verbose_name=_("Category"), on_delete=models.CASCADE)
#
#     objects = CategoryManager()
#
#     class Meta:
#         verbose_name = _("Sub-Category")
#         verbose_name_plural = _("Sub-Categories")
#
#     def __str__(self):
#         return self.sub_category + " (" + self.category.category + ")"

class ProgressManager(models.Manager):

    def new_progress(self, user):
        new_progress = self.create(user=user,
                                   score="")
        new_progress.save()
        return new_progress


class Progress(models.Model):
    """
    Progress is used to track an individual signed in users score on different
    quiz's and categories

    Data stored in csv using the format:
        category, score, possible, category, score, possible, ...
    """
    user = models.OneToOneField(settings.AUTH_USER_MODEL, verbose_name=_("User"), on_delete=models.CASCADE)

    score = models.CharField(max_length=1024,
                             verbose_name=_("Score"),
                             validators=[validate_comma_separated_integer_list])

    objects = ProgressManager()

    class Meta:
        verbose_name = _("User Progress")
        verbose_name_plural = _("User progress records")

    @property
    def list_all_cat_scores(self):
        """
        Returns a dict in which the key is the category name and the item is
        a list of three integers.

        The first is the number of questions correct,
        the second is the possible best score,
        the third is the percentage correct.

        The dict will have one key for every category that you have defined
        """
        score_before = self.score
        output = {}

        for cat in CourseInfo.objects.all():
            to_find = re.escape(cat.Course_Name) + r",(\d+),(\d+),"
            #  group 1 is score, group 2 is highest possible

            match = re.search(to_find, self.score, re.IGNORECASE)

            if match:
                score = int(match.group(1))
                possible = int(match.group(2))

                try:
                    percent = int(round((float(score) / float(possible))
                                        * 100))
                except:
                    percent = 0

                output[cat.Course_Name] = [score, possible, percent]

            else:  # if category has not been added yet, add it.
                self.score += cat.Course_Name + ",0,0,"
                output[cat.Course_Name] = [0, 0]

        if len(self.score) > len(score_before):
            # If a new category has been added, save changes.
            self.save()

        return output

    def update_score(self, question, score_to_add=0, possible_to_add=0):
        """
        Pass in question object, amount to increase score
        and max possible.

        Does not return anything.
        """
        # category_test = Category.objects.filter(category=question.category) \
        #     .exists()

        # if any([item is False for item in [category_test,
        if any([item is False for item in [ \
                score_to_add,
            possible_to_add,
            isinstance(score_to_add, int),
            isinstance(possible_to_add, int)]]):
            return _("error"), _("category does not exist or invalid score")

        to_find = re.escape(str("")) + \
                  r",(?P<score>\d+),(?P<possible>\d+),"

        match = re.search(to_find, self.score, re.IGNORECASE)

        if match:
            updated_score = int(match.group('score')) + abs(score_to_add)
            updated_possible = int(match.group('possible')) + \
                               abs(possible_to_add)

            new_score = ",".join(
                [

                    str(updated_score),
                    str(updated_possible), ""
                ])

            # swap old score for the new one
            self.score = self.score.replace(match.group(), new_score)
            self.save()

        else:
            #  if not present but existing, add with the points passed in
            self.score += ",".join(
                [

                    str(score_to_add),
                    str(possible_to_add),
                    ""
                ])
            self.save()

    def show_exams(self):
        """
        Finds the previous quizzes marked as 'exam papers'.
        Returns a queryset of complete exams.
        """
        return Sitting.objects.filter(user=self.user, complete=True)


class QuestionInheritanceManager(InheritanceManager):
    # def get_queryset(self):
    #    return super().get_queryset().filter(cent_code=request.user.center_code)
    pass


@python_2_unicode_compatible
class Question(models.Model):
    """
    Base class for all question types.
    Shared properties placed here.
    """

    # quiz = models.ManyToManyField(Quiz,
    #                               verbose_name=_("Quiz"),
    #                               blank=True)

    figure = models.ImageField(upload_to='uploads/%Y/%m/%d',
                               blank=True,
                               null=True,
                               verbose_name=_("Figure"))

    content = models.CharField(max_length=1000,
                               blank=False,
                               help_text=_("Enter the question text that "
                                           "you want displayed"),
                               verbose_name=_('Question'))

    score = models.IntegerField(
        default=1,
        help_text=_("Full score for the question"),
        verbose_name=_("Score"))

    course_code = models.ForeignKey(CourseInfo,
                                    verbose_name=_("CourseInfo"),
                                    blank=True,
                                    null=True,
                                    on_delete=models.CASCADE)

    explanation = models.TextField(max_length=2000,
                                   blank=True,
                                   help_text=_("Explanation to be shown "
                                               "after the question has "
                                               "been answered."),
                                   verbose_name=_('Explanation'))

    cent_code = models.ForeignKey(
        CenterInfo, null=True, blank=True,
        verbose_name=_("Center Code"), on_delete=models.CASCADE)

    objects = InheritanceManager()

    class Meta:
        verbose_name = _("Question")
        verbose_name_plural = _("Questions")
        # ordering = ['category']

    def __str__(self):
        return self.content

    def is_saq(self):
        return type(self) is SA_Question

    def is_mcq(self):
        return type(self) is MCQuestion

    def is_tfq(self):
        return type(self) is TF_Question


class MCQuestion(Question):
    answer_order = models.CharField(
        max_length=30, null=True, blank=True,
        default='content',
        choices=ANSWER_ORDER_OPTIONS,
        help_text=_("The order in which multichoice "
                    "answer options are displayed "
                    "to the user"),
        verbose_name=_("Answer Order"))

    def check_if_correct(self, guess):
        if guess:
            if Answer.objects.filter(id=int(guess)).exists():
                answer = Answer.objects.get(id=int(guess))
                if answer.correct is True:
                    return True
        return False

    def order_answers(self, queryset):
        if self.answer_order == 'content':
            return queryset.order_by('content')
        if self.answer_order == 'random':
            return queryset.order_by('?')
        if self.answer_order == 'none':
            return queryset.order_by()
        return queryset

    def get_answers(self):
        return self.order_answers(Answer.objects.filter(question=self))

    def get_answers_list(self):
        return [(answer.id, answer.content) for answer in
                self.order_answers(Answer.objects.filter(question=self))]

    def get_correct_answer(self):
        correct_ans = list(Answer.objects.filter(question=self, correct=True).values_list('content', flat=True))
        return ", ".join( repr(e) for e in correct_ans)

    def answer_choice_to_string(self, guess):
        return Answer.objects.get(id=guess).content

    def correct_option_limit_check(self):
        correct_limit = 2
        correct_answers = Answer.objects.filter(question=self, correct=True)
        if correct_answers.count() < correct_limit:
            return True
        else:
            return False

    def get_num_correct_options(self):
        return Answer.objects.filter(question=self, correct=True).count()

    class Meta:
        verbose_name = _("Multiple Choice Question")
        verbose_name_plural = _("Multiple Choice Questions")

    def get_absolute_url(self):
        return reverse('mcquestion_detail', args=(self.pk,))

    def get_update_url(self):
        return reverse('mcquestion_update', args=(self.pk,))


class TF_Question(Question):
    correct = models.BooleanField(blank=False,
                                  default=False,
                                  help_text=_("Tick this if the question "
                                              "is true. Leave it blank for"
                                              " false."),
                                  verbose_name=_("Correct"))

    def check_if_correct(self, guess):
        if guess == "True":
            guess_bool = True
        elif guess == "False":
            guess_bool = False
        else:
            return False

        if guess_bool == self.correct:
            return True
        else:
            return False

    def get_answers(self):
        return [{'correct': self.check_if_correct("True"),
                 'content': 'True'},
                {'correct': self.check_if_correct("False"),
                 'content': 'False'}]

    def get_answers_list(self):
        return [(True, True), (False, False)]

    def answer_choice_to_string(self, guess):
        return str(guess)

    class Meta:
        verbose_name = _("True/False Question")
        verbose_name_plural = _("True/False Questions")
        # ordering = ['category']

    def get_absolute_url(self):
        return reverse('tfquestion_detail', args=(self.pk,))

    def get_update_url(self):
        return reverse('tfquestion_update', args=(self.pk,))


# modelss___________________________________________________________
class SA_Question(Question):

    def check_if_correct(self, guess):
        return True

    def get_answers(self):
        return False

    def get_answers_list(self):
        return False

    def answer_choice_to_string(self, guess):
        return str(guess)

    def __str__(self):
        return self.content

    class Meta:
        verbose_name = _("Short Answer Question")
        verbose_name_plural = _("Short Answer Questions")

    def get_absolute_url(self):
        return reverse('saquestion_detail', args=(self.pk,))

    def get_update_url(self):
        return reverse('saquestion_update', args=(self.pk,))


@python_2_unicode_compatible
class Quiz(models.Model):
    mcquestion = models.ManyToManyField(
        MCQuestion,
        verbose_name=_("Multiple Choice Question"),
        help_text=_("You can select multiple questions by holding ctrl key on Windows and Command⌘ key on MAC.")
    )
    tfquestion = models.ManyToManyField(
        TF_Question,
        verbose_name=_("True/False Question"),
        help_text=_("You can select multiple questions by holding ctrl key on Windows and Command⌘ key on MAC.")
    )
    saquestion = models.ManyToManyField(
        SA_Question,
        verbose_name=_("Short Answer Type Question"),
        help_text=_("You can select multiple questions by holding ctrl key on Windows and Command⌘ key on MAC.")
    )

    # start_time=
    title = models.CharField(
        verbose_name=_("Title"),
        max_length=255, blank=False)

    description = models.TextField(
        verbose_name=_("Description"),
        blank=True, help_text=_("a description of the quiz"))

    url = models.SlugField(
        max_length=60, blank=True, null=True,
        help_text=_("a user friendly url"),
        verbose_name=_("user friendly url"))

    course_code = models.ForeignKey(
        CourseInfo,
        verbose_name=_("Course"), on_delete=models.CASCADE)

    cent_code = models.ForeignKey(
        CenterInfo, null=True, blank=True,
        verbose_name=_("Center Code"), on_delete=models.CASCADE)

    duration = models.IntegerField(
        null=True, blank=True,
        default=1800,
        help_text=_("Time limit for quiz"),
        verbose_name=_("Time limit for quiz"))

    pre_test = models.BooleanField(
        help_text=_("Before the chapter"),
        default=False
    )
    post_test = models.BooleanField(
        help_text=_("After the chapter"),
        default=False
    )
    created_date = models.DateTimeField(
        auto_now_add=True
    )
    updated_date = models.DateTimeField(
        auto_now=True
    )
    chapter_code = models.ForeignKey(
        ChapterInfo, null=True, blank=True,
        verbose_name=_("Chapter"), on_delete=models.CASCADE)

    def duration_HHmm(self):
        sec = self.duration.total_seconds()
        return '%02d:%02d' % (int((sec / 3600) % 3600), int((sec / 60) % 60))

    # in template just use {{ < model >.duration_HHmm}} instead of {{ < model >.duration}}.

    random_order = models.BooleanField(
        blank=False, default=False,
        verbose_name=_("Random Order"),
        help_text=_("Display the questions in "
                    "a random "))

    # max_questions = models.PositiveIntegerField(
    #     blank=True, null=True, verbose_name=_("Max Questions"),
    #     help_text=_("Number of questions to be answered on each attempt."))

    answers_at_end = models.BooleanField(
        blank=False, default=False,
        help_text=_("Correct answer is displayed at the end."),
        verbose_name=_("Answers at end"))

    exam_paper = models.BooleanField(
        blank=False, default=False,
        help_text=_("If yes, the result of attempts by user will be"
                    " stored "),
        verbose_name=_("Exam Paper"))

    single_attempt = models.BooleanField(
        blank=False, default=True,
        help_text=_("If yes, only one attempt by"
                    " a user will be permitted."
                    ),
        verbose_name=_("Single Attempt"))

    pass_mark = models.SmallIntegerField(
        blank=True, default=40,
        verbose_name=_("Pass Mark"),
        help_text=_("Percentage required to pass exam."),
        validators=[MaxValueValidator(100)])

    success_text = models.TextField(
        blank=True, help_text=_("Displayed if user passes."),
        verbose_name=_("Success Text"), default=_("Congratulations!!!."))

    fail_text = models.TextField(
        verbose_name=_("Fail Text"), default=_("Sorry, You Failed!."),
        blank=True, help_text=_("Displayed if user fails."))

    draft = models.BooleanField(
        blank=True, default=False,
        verbose_name=_("Draft"),
        help_text=_("If checked, the quiz is not displayed to the student"
                    ))
    negative_marking = models.BooleanField(
        blank=True, default=False,
        verbose_name=_("Negative Marking"),
        help_text=_("If checked, incorrect answers will have negative marking")
    )
    negative_percentage = models.IntegerField(
        null=True, blank=True, default=0,
        help_text=_("Percentage of total marks to use for negative marking"),
        verbose_name=_("Negative Marking Percentage"))

    mcquestion_order = models.CharField(max_length=1024, null=True, blank=True)
    saquestion_order = models.CharField(max_length=1024, null=True, blank=True)
    tfquestion_order = models.CharField(max_length=1024, null=True, blank=True)

    def get_absolute_url(self):
        return reverse('quiz_update', args=(self.pk,))

    def get_update_url(self):
        return reverse('quiz_update', args=(self.pk,))

    def save(self, force_insert=False, force_update=False, *args, **kwargs):
        # self.url = re.sub('\s+', '-', self.url).lower()
        #
        # self.url = ''.join(letter for letter in self.url if
        #                    letter.isalnum() or letter == '-')

        if self.exam_paper is True:
            # self.single_attempt = True
            self.chapter_code = None
            self.answers_at_end = False
        else:
            self.answers_at_end = True

        if self.pass_mark is None:
            self.pass_mark = 0

        if self.pass_mark > 100:
            raise ValidationError('%s is above 100' % self.pass_mark)

        super(Quiz, self).save(force_insert, force_update, *args, **kwargs)

    def question_count(self):
        return len(self.mcquestion.all()) + len(self.tfquestion.all()) + len(self.saquestion.all())

    class Meta:
        verbose_name = _("Quiz")
        verbose_name_plural = _("Quizzes")

    def __str__(self):
        return self.title

    def get_mcquestions(self):
        return self.mcquestion_set.all()

    def get_tfquestions(self):
        return self.tfquestion_set.all()

    def get_saquestions(self):
        return self.saquestion.all()

    def has_mcqs(self):
        return (self.mcquestion.count() > 0)

    def has_tfqs(self):
        return (self.tfquestion.count() > 0)

    def has_saqs(self):
        return (self.saquestion.count() > 0)
    
    def has_sittings(self):
        if Sitting.objects.filter(quiz=self):
            return True
        return False


    # def get_questions(self):
    #    return self.question_set.all()

    def get_questions(self):
        question_ids = self._question_ids()
        mcquestions = sorted(
            self.mcquestion.filter(id__in=question_ids),
            key=lambda q: question_ids.index(q.id))
        tfquestions = sorted(
            self.tfquestion.filter(id__in=question_ids),
            key=lambda q: question_ids.index(q.id))
        saquestions = sorted(
            self.saquestion.filter(id__in=question_ids),
            key=lambda q: question_ids.index(q.id))
        questions = mcquestions + tfquestions + saquestions

        return questions

    @property
    def get_max_score(self):
        # return self.get_mcquestions().count() + self.get_tfquestions().count() + self.get_questions().count()
        score = 0
        for q in self.mcquestion.all():
            score += q.score
        for q in self.tfquestion.all():
            score += q.score
        for q in self.saquestion.all():
            score += q.score
        return score

    def anon_score_id(self):
        return str(self.id) + "_score"

    def anon_q_list(self):
        return str(self.id) + "_q_list"

    def anon_q_data(self):
        return str(self.id) + "_data"

    # User Quiz submission can be checked by quiz.sitting_set.all.count > 0.
    # Each completed quiz will have the user sitting
    # def can_take(self, user):
    #     if self.draft and not user.has_perm('quiz.change_quiz'):
    #         raise PermissionDenied
    #
    #     try:
    #         self.logged_in_user = user.is_authenticated()
    #     except TypeError:
    #         self.logged_in_user = user.is_authenticated
    #
    #     if self.logged_in_user:
    #         self.sitting = Sitting.objects.user_sitting(
    #             user, self)
    #
    #     return self.sitting


@python_2_unicode_compatible
class Answer(models.Model):
    question = models.ForeignKey(MCQuestion, verbose_name=_("Question"), on_delete=models.CASCADE)

    content = models.CharField(max_length=1000,
                               blank=False,
                               help_text=_("Enter the answer text that "
                                           "you want displayed"),
                               verbose_name=_("Option"))

    correct = models.BooleanField(blank=False,
                                  default=False,
                                  help_text=_("Is this a correct answer?"),
                                  verbose_name=_("Correct"))

    def __str__(self):
        return self.content

    class Meta:
        verbose_name = _("Answer")
        verbose_name_plural = _("Answers")


class SittingManager(models.Manager):

    def new_sitting(self, user, quiz):
        if quiz.random_order is True:
            mcquestion_set = quiz.mcquestion.all().order_by('?')
            tfquestion_set = quiz.tfquestion.all().order_by('?')
            saquestion_set = quiz.saquestion.all().order_by('?')
            mcquestion_set = [item.id for item in mcquestion_set]
            tfquestion_set = [item.id for item in tfquestion_set]
            saquestion_set = [item.id for item in saquestion_set]
        else:
            if quiz.mcquestion_order:
                mcquestion_set = [int(x) for x in quiz.mcquestion_order.split(",")]
            else:
                mcquestion_set = quiz.mcquestion.all()
                mcquestion_set = [item.id for item in mcquestion_set]

            if quiz.tfquestion_order:
                tfquestion_set = [int(x) for x in quiz.tfquestion_order.split(",")]
            else:
                tfquestion_set = quiz.tfquestion.all()
                tfquestion_set = [item.id for item in tfquestion_set]

            if quiz.saquestion_order:
                saquestion_set = [int(x) for x in quiz.saquestion_order.split(",")]
            else:
                saquestion_set = quiz.saquestion.all()
                saquestion_set = [item.id for item in saquestion_set]
            

        if (len(mcquestion_set) == 0 and len(tfquestion_set) == 0 and len(saquestion_set) == 0):
            raise ImproperlyConfigured('Question set of the quiz is empty. Please configure questions properly')

        # if quiz.max_questions and quiz.max_questions < len(mcquestion_set):
        #     mcquestion_set = mcquestion_set[:quiz.max_questions]
        # if quiz.max_questions and quiz.max_questions < len(tfquestion_set):
        #     tfquestion_set = tfquestion_set[:quiz.max_questions]
        # if quiz.max_questions and quiz.max_questions < len(saquestion_set):
        #     saquestion_set = saquestion_set[:quiz.max_questions]

        mcquestions, tfquestions, saquestions = "", "", ""

        if mcquestion_set:
            mcquestions = ",".join(map(str, mcquestion_set)) + ","
        if tfquestion_set:
            tfquestions = ",".join(map(str, tfquestion_set)) + ","
        if saquestion_set:
            saquestions = ",".join(map(str, saquestion_set)) + ","

        questions = mcquestions + tfquestions + saquestions

        new_sitting = self.create(user=user,
                                  quiz=quiz,
                                  question_order=questions,
                                  question_list=questions,
                                  incorrect_questions="",
                                  current_score=0,
                                  complete=False,
                                  user_answers='{}')
        return new_sitting

    def user_sitting(self, user, quiz):
        if quiz.single_attempt is True and self.filter(user=user,
                                                       quiz=quiz,
                                                       complete=True) \
                .exists():
            return False

        try:
            sitting = self.get(user=user, quiz=quiz, complete=False)
        except Sitting.DoesNotExist:
            sitting = self.new_sitting(user, quiz)
        except Sitting.MultipleObjectsReturned:
            sitting = self.filter(user=user, quiz=quiz, complete=False)[0]
        return sitting


class Sitting(models.Model):
    """
    Used to store the progress of logged in users sitting a quiz.
    Replaces the session system used by anon users.

    Question_order is a list of integer pks of all the questions in the
    quiz, in order.

    Question_list is a list of integers which represent id's of
    the unanswered questions in csv format.

    Incorrect_questions is a list in the same format.

    Sitting deleted when quiz finished unless quiz.exam_paper is true.

    User_answers is a json object in which the question PK is stored
    with the answer the user gave.
    """

    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_("User"), on_delete=models.CASCADE)

    quiz = models.ForeignKey(Quiz, verbose_name=_("Quiz"), on_delete=models.CASCADE)

    question_order = models.CharField(
        max_length=1024,
        verbose_name=_("Question Order"),
        validators=[validate_comma_separated_integer_list])

    question_list = models.CharField(
        max_length=1024,
        verbose_name=_("Question List"),
        validators=[validate_comma_separated_integer_list])

    score_list = models.CharField(
        max_length=1024,
        null=True, blank=True,
        verbose_name=_("Score List"),
        validators=[])

    incorrect_questions = models.CharField(
        max_length=1024,
        blank=True,
        verbose_name=_("Incorrect questions"),
        validators=[validate_comma_separated_integer_list])

    current_score = models.IntegerField(verbose_name=_("Current Score"))

    complete = models.BooleanField(default=False, blank=False,
                                   verbose_name=_("Complete"))

    user_answers = models.TextField(blank=True, default='{}',
                                    verbose_name=_("User Answers"))

    start = models.DateTimeField(auto_now_add=True,
                                 verbose_name=_("Start"))
    time_elapsed = models.IntegerField(
        null=True, blank=True,
        default=0,
    )
    end = models.DateTimeField(null=True, blank=True, verbose_name=_("End"))

    objects = SittingManager()

    class Meta:
        permissions = (("view_sittings", _("Can see completed exams.")),)

    def get_first_question(self, question_index=None):
        """
        Returns the next question.
        If no question is found, returns False
        Does NOT remove the question from the front of the list.
        """
        if not self.question_list:
            return False
        if not question_index:
            first, _ = self.question_list.split(',', 1)
        else:
            first = self.question_order.split(',')[question_index-1]
        question_id = int(first)

        return Question.objects.get_subclass(id=question_id)

    def remove_first_question(self, question_id=None):
        if not self.question_list:
            return
        if question_id:
            x = self.question_list.split(',')
            x.remove(question_id)
            x = ','.join(x)
            self.question_list = x

        else:
            _, others = self.question_list.split(',', 1)
            self.question_list = others
        self.save()

    def add_to_score(self, points):
        self.current_score += int(points)
        self.save()

    @property
    def get_current_score(self):
        return self.current_score

    def _question_ids(self):
        return [int(n) for n in self.question_order.split(',') if n]

    @property
    def get_score_correct(self):
        totalmcq_score = 0.0
        totaltfq_score = 0.0
        totalsaq_score = 0.0
        user_answers = json.loads(self.user_answers)
        for i in self.quiz.mcquestion.all():
            mcq_user_ans = user_answers.get(str(i.id))
            num_correct_options = i.get_num_correct_options()
            per_score = i.score / num_correct_options
            if mcq_user_ans:                                    # if no answer, just add 0, so just ignore
                if not (isinstance(mcq_user_ans, list)):        # For old data without list
                    mcq_user_ans = [mcq_user_ans]
                for ans in mcq_user_ans:
                    if i.check_if_correct(ans):                 # multi-ans-effect
                        totalmcq_score += per_score
                    elif self.quiz.negative_marking:
                        totalmcq_score -= float(per_score * self.quiz.negative_percentage) / 100
        for j in self.quiz.tfquestion.all():
            tfq_user_ans = user_answers.get(str(j.id))
            if j.check_if_correct(tfq_user_ans):
                totaltfq_score += j.score
            elif self.quiz.negative_marking:
                totaltfq_score -= float(j.score * self.quiz.negative_percentage) / 100
        for k in self.quiz.saquestion.all():
            i = [int(n) for n in self.question_order.split(',') if n].index(k.id)
            if self.score_list:
                score_list = str(self.score_list).split(',')
                if i < len(score_list):
                    if str(score_list[i]) and str(score_list[i]) != 'not_graded':
                        totalsaq_score += float(score_list[i])

        return totalmcq_score + totaltfq_score + totalsaq_score

        # # score = 0.0
        # # for n in self.score_list.split(','):
        # #     if (n != "") and (n != " ") and (n != "not_graded"):
        # #         score += float(n)
        # return score

    @property
    def get_percent_correct(self):
        score = self.get_score_correct
        total_score = self.quiz.get_max_score
        if score > 0 and total_score > 0:
            return round((score / total_score) * 100, 2)
        else:
            return 0
        # # dividend = float(self.current_score)
        # dividend = 0
        # for n in self.score_list.split(','):
        #     if (n != "") and (n != " ") and (n != "not_graded"):
        #         dividend += float(n)

        # # divisor = len(self._question_ids())
        # divisor = 0
        # for x in [int(n) for n in self.question_order.split(',') if n]:
        #     score = Question.objects.get(id=x).score
        #     divisor += float(score)
        # if divisor < 1:
        #     return 0  # prevent divide by zero error

        # if dividend > divisor:
        #     return 100

        # correct = float('%.2f' % ((dividend / divisor) * 100.0))

        # if correct >= 1:
        #     return correct
        # else:
        #     return 0

    def mark_quiz_complete(self):
        self.complete = True
        self.end = now()
        self.save()

    def add_incorrect_question(self, question):
        """
        Adds uid of incorrect question to the list.
        The question object must be passed in.
        """
        if len(self.incorrect_questions) > 0:
            self.incorrect_questions += ','
        self.incorrect_questions += str(question.id) + ","
        if self.complete:
            self.add_to_score(-1)
        self.save()

    @property
    def get_incorrect_questions(self):
        """
        Returns a list of non empty integers, representing the pk of
        questions
        """
        return [int(q) for q in self.incorrect_questions.split(',') if q]

    def remove_incorrect_question(self, question):
        current = self.get_incorrect_questions
        current.remove(question.id)
        self.incorrect_questions = ','.join(map(str, current))
        self.add_to_score(1)
        self.save()

    @property
    def check_if_passed(self):
        return self.get_percent_correct >= self.quiz.pass_mark

    @property
    def result_message(self):
        if self.check_if_passed:
            return self.quiz.success_text
        else:
            return self.quiz.fail_text

    def add_user_answer(self, question, guess):
        current = json.loads(self.user_answers)
        current[str(question.id)] = guess
        self.user_answers = json.dumps(current)
        self.save()

    def get_questions(self, with_answers=False):
        question_ids = self._question_ids()
        mcquestions = sorted(
            self.quiz.mcquestion.filter(id__in=question_ids),
            key=lambda q: question_ids.index(q.id))
        tfquestions = sorted(
            self.quiz.tfquestion.filter(id__in=question_ids),
            key=lambda q: question_ids.index(q.id))
        saquestions = sorted(
            self.quiz.saquestion.filter(id__in=question_ids),
            key=lambda q: question_ids.index(q.id))
        questions = mcquestions + tfquestions + saquestions

        if with_answers:
            user_answers = json.loads(self.user_answers)
            for q in questions:
                user_ans = user_answers.get(str(q.id), False)
                if user_ans:
                    if isinstance(q, MCQuestion):
                        if (isinstance(question_name_value, list)):
                            q.user_answer = Answer.objects.filter(
                                            id__in=[int(a) for a in user_ans]).values_list('content', flat=True)    # multi-ans-effect
                        else:               # old data case
                            q.user_answer = Answer.objects.get(id=int(user_ans)).content 
                    else:
                        q.user_answer = user_ans
                    
                    if isinstance(q, SA_Question):
                        i = [int(n) for n in json.loads(self.user_answers).keys() if n].index(q.id)
                        score_list = str(self.score_list).split(',')
                        if i < len(score_list):
                            q.score_obtained = score_list[i]
                            q.ans_correct = True
                            if str(q.score_obtained) == '0':
                                 q.ans_correct = False
                        else:
                            q.score_obtained = "not_graded"
                            q.ans_correct = True
                    elif isinstance(q, MCQuestion):
                        num_correct_options = q.get_num_correct_options() # get number of correct options
                        num_options = q.get_answers().count()
                        per_score = q.score / num_correct_options
                        guess = user_ans
                        if not (isinstance(guess, list)):
                            guess = [guess]         #### support for old sitting data where there won't be list.
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
                            if q.check_if_correct(g):
                                score += per_score
                            else:
                                is_correct = False          ###### user selected wrong answer
                                if self.quiz.negative_marking:
                                    score -= float(per_score * self.quiz.negative_percentage) / 100.0
                                else:
                                    score += 0
                        # print("guess: ",guess, score, type(guess))
                        num_correct_guess = sum([q.check_if_correct(g) for g in guess])
                        if not (num_correct_options == num_correct_guess):
                            is_correct = False
                                    
                        q.score_obtained = score
                        q.ans_correct = is_correct
                                        
                    else:
                        if q.check_if_correct(user_ans):
                            q.score_obtained = q.score
                            q.ans_correct = True
                        else:
                            if self.quiz.negative_marking:
                                q.score_obtained = -float(q.score * self.quiz.negative_percentage) / 100
                            else:
                                q.score_obtained = 0
                            q.ans_correct = False
                else:
                    q.user_answer = ' '
                    q.score_obtained  = 0

                # # q.user_answer = user_answers[str(q.id)]
                # q.user_answer = user_answers.get(str(q.id), False)
                # i = [int(n) for n in self.question_order.split(',') if n].index(q.id)
                # if i < len([s for s in self.score_list.split(',') if s]):
                #     score = [s for s in self.score_list.split(',') if s][i]
                # else:
                #     score = "not_graded"
                # q.score_obtained = score

        return questions

    @property
    def questions_with_user_answers(self):          # multi-ans-effect for child
        return {
            q: q.user_answer for q in self.get_questions(with_answers=True)
        }

    @property
    def get_max_score(self):
        # return len(self._question_ids())
        total = 0
        for x in [int(n) for n in self.question_order.split(',') if n]:
            score = Question.objects.get(id=x).score
            total += score
        return total

    def progress(self):
        """
        Returns the number of questions answered so far and the total number of
        questions.
        """
        answered = len(json.loads(self.user_answers))
        total = self.get_max_score
        total_questions = len(self.question_order.split(',')[:-1])
        return answered, total, total_questions

    def get_progress(self):
        answered = len(json.loads(self.user_answers))
        total = len(self._question_ids())
        return answered * 100 / total

    def get_mcq_score(self, mcq):
        user_answers = json.loads(self.user_answers)
        guess = user_answers.get(str(mcq.id), False)
        if guess and not (isinstance(guess, list)):
            guess = [guess]         #### support for old sitting data where there won't be list.
        if guess:
            num_correct_options = mcq.get_num_correct_options() # get number of correct options
            num_options = mcq.get_answers().count()
            per_score = mcq.score / num_correct_options
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
                if mcq.check_if_correct(g):
                    score += per_score
                else:
                    is_correct = False          ###### user selected wrong answer
                    if self.quiz.negative_marking:
                        score -= float(per_score * self.quiz.negative_percentage) / 100.0
                    else:
                        score += 0

            num_correct_guess = sum([mcq.check_if_correct(g) for g in guess])
            if not (num_correct_options == num_correct_guess):
                is_correct = False                  ######### user didn't selected all answers
                        
            return score, is_correct
        else:
            return 0, False