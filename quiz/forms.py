from django import forms
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.forms.widgets import RadioSelect, Textarea
from django.urls import reverse_lazy
from django.utils.translation import gettext as _
# from quiz import admin
from django_addanother.widgets import AddAnotherWidgetWrapper

from quiz.models import Quiz, MCQuestion, TF_Question, SA_Question, Answer
from django.forms import inlineformset_factory


# class AnswerInline(admin.TabularInline):
#     model = Answer

class QuestionForm(forms.Form):
    def __init__(self, question, *args, **kwargs):
        super(QuestionForm, self).__init__(*args, **kwargs)
        choice_list = [x for x in question.get_answers_list()]
        self.fields["answers"] = forms.ChoiceField(choices=choice_list,
                                                   widget=RadioSelect)


class SAForm(forms.Form):
    def __init__(self, question, *args, **kwargs):
        super(SAForm, self).__init__(*args, **kwargs)
        self.fields["answers"] = forms.CharField(
            widget=Textarea(attrs={'style': 'width:100%'}))


class QuizForm(forms.ModelForm):

    # mcquestion = forms.ModelMultipleChoiceField(
    #     queryset=MCQuestion.objects.all(),
    #     initial=[],
    #     required=False,
    #     # label=_("Questions"),
    #     widget= AddAnotherWidgetWrapper(
    #             forms.SelectMultiple,
    #             reverse_lazy('mcquestion_create'),
    #         ))

    # override __init__() to
    # remove "required" from question field
    # and hide friendly url for now????
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['mcquestion'].required = False
        self.fields['tfquestion'].required = False
        self.fields['saquestion'].required = False
        self.fields['cent_code'].required = False

        # self.fields['url'].required = False
        # self.fields['url'].widget = forms.HiddenInput()
        # last_quiz = Quiz.objects.last()
        # if(last_quiz):
        #    self.fields['url'].initial = "quiz" + str(last_quiz.id)
        #    self.fields['title'].initial = "quiz" + str(last_quiz.id)
        # else:
        #    self.fields['url'].initial = "quiz0"
        #    self.fields['title'].initial = "quiz0"

    class Meta:
        model = Quiz
        fields = '__all__'

    # override clean() to
    # add custom validation such that atleast
    # one of the question must be present
    def clean(self):
        cleaned_data = super().clean()
        mq = cleaned_data.get("mcquestion")
        tq = cleaned_data.get("tfquestion")
        eq = cleaned_data.get("saquestion")
        if not (mq or tq or eq):
            raise forms.ValidationError(
                "Please Select Atleast One Question"
            )
        return cleaned_data


class MCQuestionForm(forms.ModelForm):
    class Meta:
        model = MCQuestion
        fields = '__all__'

    # quiz = forms.ModelMultipleChoiceField(
    #     queryset=Quiz.objects.all(),
    #     required=False,
    #     # label=_("Questions"),
    #     widget=FilteredSelectMultiple(verbose_name=_("Quizzes"), is_stacked=False))


class TFQuestionForm(forms.ModelForm):
    class Meta:
        model = TF_Question
        fields = '__all__'

    # quiz = forms.ModelMultipleChoiceField(
    #     queryset=Quiz.objects.all(),
    #     required=False,
    #     # label=_("Questions"),
    #     widget=FilteredSelectMultiple(verbose_name=_("Quizzes"), is_stacked=False))


class SAQuestionForm(forms.ModelForm):
    class Meta:
        model = SA_Question
        fields = '__all__'

    # quiz = forms.ModelMultipleChoiceField(
    #     queryset=Quiz.objects.all(),
    #     required=False,
    #     # label=_("Questions"),
    #     widget=FilteredSelectMultiple(verbose_name=_("Quizzes"), is_stacked=False))


class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = '__all__'


AnsFormset = inlineformset_factory(MCQuestion, Answer, form=AnswerForm, fields=['content', 'correct'], extra=1, )


class QuizForm1(forms.ModelForm):
    class Meta:
        model = Quiz
        fields = ['title', 'description', 'url', 'course_code', 'cent_code', 'duration']


class QuizForm2(forms.ModelForm):
    class Meta:
        model = Quiz
        fields = ['pre_test', 'post_test', 'chapter_code', 'answers_at_end',
                  'exam_paper', 'single_attempt', 'random_order', 'pass_mark', 'success_text', 'fail_text', 'draft']


class QuizForm3(forms.ModelForm):
    class Meta:
        model = Quiz
        fields = ['mcquestion', 'tfquestion', 'saquestion']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['mcquestion'].required = False
        self.fields['tfquestion'].required = False
        self.fields['saquestion'].required = False
