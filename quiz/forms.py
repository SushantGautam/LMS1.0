from django import forms
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.forms.widgets import RadioSelect, Textarea
from django.urls import reverse_lazy
from django.utils.translation import gettext as _
# from quiz import admin
from django_addanother.widgets import AddAnotherWidgetWrapper

from quiz.models import Quiz, MCQuestion, TF_Question, SA_Question, Answer
from django.forms import inlineformset_factory

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, Div, HTML, Field, Button
from crispy_forms.bootstrap import AppendedText, PrependedText, StrictButton


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


from django.utils.safestring import mark_safe


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
    class Meta:
        model = Quiz
        fields = ['title', 'description', 'random_order', 'success_text', 'fail_text', 'mcquestion', 'tfquestion',
                  'saquestion']

    def __init__(self, *args, **kwargs):
        course_id = kwargs.pop('course_id')
        mcqueryset = MCQuestion.objects.filter(course_code=course_id)
        tfqueryset = TF_Question.objects.filter(course_code=course_id)
        saqueryset = SA_Question.objects.filter(course_code=course_id)
        super().__init__(*args, **kwargs)
        self.fields['mcquestion'].required = False
        self.fields['tfquestion'].required = False
        self.fields['saquestion'].required = False
        self.fields['success_text'].initial = 'Congratulations!!!'
        self.fields['fail_text'].initial = 'Sorry!'
        self.fields['mcquestion'].queryset = mcqueryset
        self.fields['tfquestion'].queryset = tfqueryset
        self.fields['saquestion'].queryset = saqueryset

        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Row(
                Column('title', css_class='form-group col-md-4 mb-0'),
                Column('description', css_class='form-group col-md-4 mb-0'),
                HTML('''<div class=col-md-4></div>'''),
                css_class='form-row'
            ),
            Row(
                Column('success_text', css_class='form-group col-md-6 mb-0'),
                HTML('''<div class=col-md-6></div>'''),
                css_class='form-row'
            ),
            Field(PrependedText('fail_text',
                                mark_safe('<span class="glyphicon glyphicon-envelope"></span>'),
                                placeholder="Enter Email")),
            'random_order', 'mcquestion', 'tfquestion', 'saquestion'
        )

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
        fields = ['title', 'course_code', 'description']


class QuizForm2(forms.ModelForm):
    class Meta:
        model = Quiz
        fields = ['chapter_code', 'pre_test', 'post_test', 'answers_at_end', 'random_order',
                  'single_attempt', 'draft', 'exam_paper', 'duration',
                  'pass_mark', 'success_text', 'fail_text']

    def clean(self):
        cleaned_data = super().clean()
        exam_val = cleaned_data.get("exam_paper")
        pre_val = cleaned_data.get("pre_test")
        post_val = cleaned_data.get("post_test")
        if not exam_val:
            if not (pre_val or post_val):
                raise forms.ValidationError(
                    "Please Select at least One Quiz Type"
                )
        else:
            if pre_val or post_val:
                raise forms.ValidationError(
                    "Exam cannot be pre/post chapter"
                )
            else:
                pass

        if not (pre_val or post_val) and not (exam_val):
            raise forms.ValidationError(
                "Please Select Atleast One Question"
            )
        return cleaned_data

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['exam_paper'].initial = False
        self.fields['success_text'].initial = "Congratulations. !!!"
        self.fields['fail_text'].initial = "Sorry. !!!"

        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.label_class = 'quiz-add-label'
        self.helper.layout = Layout(

             Row(
                Column('chapter_code', css_class='form-group col-md-4 mb-0'),
                Column(
                    PrependedText(
                        'success_text',
                        '<i class="fa fa-edit"></i>',
                        rows='1'
                    ),
                    css_class='form-group col-md-4 mb-0'
                ),
                Column(
                    PrependedText(
                        'fail_text',
                        '<i class="fa fa-edit"></i>',
                        rows='1'
                    ),
                    css_class='form-group col-md-4 mb-0'
                ),
                css_class='form-row'
            ),
            HTML('''<hr size="10">'''),


            HTML('''<label class=quiz-add-label>Quiz Type</label>'''),
            Row(
                Column('pre_test', css_class='form-group col-md-4 mb-0'),
                Column('post_test', css_class='form-group col-md-4 mb-0'),
                Column('exam_paper', css_class='form-group col-md-4 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('duration', css_class='form-group col-md-4 mb-0'),
                Column('pass_mark', css_class='form-group col-md-4 mb-0'),
                Column(css_class='form-group col-md-4 mb-0'),

                css_class='form-row'
            ),
           
            # HTML('''<hr size="10">'''),
            HTML('''<hr size="10">'''),
            HTML('''<label class=quiz-add-label>Quiz Features</label>'''),
            Row(
                Column('random_order', css_class='form-group col-md-4 mb-0'),
                Column('single_attempt', css_class='form-group col-md-4 mb-0'),
                Column('draft', css_class='form-group col-md-4 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column(css_class='col-md-4 mb-0'),
                Column(css_class='col-md-4 mb-0'),
                Column(
                    StrictButton('Previous', name='wizard_goto_step', value='form1', css_class='add-mcq',
                                 type='submit'),
                    StrictButton('Next', css_class='add-mcq', type='submit'),
                    css_class='col-md-4 mb-0 text-right'
                ),
                css_class='form-row'
            ),
        )


class QuizForm3(forms.ModelForm):
    class Meta:
        model = Quiz
        fields = ['mcquestion', 'tfquestion', 'saquestion']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['mcquestion'].required = False
        self.fields['tfquestion'].required = False
        self.fields['saquestion'].required = False

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
