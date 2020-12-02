import datetime
from functools import partial

from crispy_forms.bootstrap import PrependedText, StrictButton
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Div, HTML
from django import forms
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.forms import inlineformset_factory
from django.forms.models import ModelChoiceIterator
from django.forms.widgets import RadioSelect, Textarea
from django.utils.translation import gettext as _

from WebApp.models import CourseInfo
from quiz.models import Quiz, MCQuestion, TF_Question, SA_Question, Answer


# from quiz import admin


# class AnswerInline(admin.TabularInline):
#     model = Answer

class QuestionForm(forms.Form):
    def __init__(self, question, answer=None, *args, **kwargs):
        super(QuestionForm, self).__init__(*args, **kwargs)
        choice_list = [x for x in question.get_answers_list()]
        # self.fields["answers"] = forms.ChoiceField(choices=choice_list,
        #                                            widget=RadioSelect)
        answerindex = None
        if answer:
            for index, x in enumerate(choice_list):
                if str(x[0]) == answer:
                    answerindex = index
                    break
        self.fields["answers"] = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple,
                                          choices=choice_list)

class MCForm(forms.Form):
    def __init__(self, question, *args, **kwargs):
        super().__init__(*args, **kwargs)
        choice_list = [x for x in question.get_answers_list()]
        # self.fields["answers"] = forms.ChoiceField(choices=choice_list,
        #                                            widget=RadioSelect)
        self.fields["answers"] = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple,
                                          choices=choice_list)

class TFForm(forms.Form):
    def __init__(self, question, *args, **kwargs):
        super().__init__(*args, **kwargs)
        choice_list = [x for x in question.get_answers_list()]
        self.fields["answers"] = forms.ChoiceField(choices=choice_list,
                                                   widget=RadioSelect, initial=choice_list[int(answerindex)] if answerindex is not None else None)

class SAForm(forms.Form):
    def __init__(self, question, answer=None, *args, **kwargs):
        super(SAForm, self).__init__(*args, **kwargs)
        self.fields["answers"] = forms.CharField(
            widget=Textarea(attrs={'style': 'width:100%'}), initial=answer)


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
    # and hide friendly url for now????'exam_paper', 'duration', 'pass_mark', 'negative_marking',
    #                   'negative_percentage',

    class Meta:
        model = Quiz
        fields = ['mcquestion', 'tfquestion', 'saquestion', 'title', 'description', 'duration', 'pass_mark',
                  'negative_marking',
                  'negative_percentage', 'random_order', 
                  'mcquestion_order', 'saquestion_order', 'tfquestion_order']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4, }),
        }
        labels = {
            "mcquestion": "Multiple Choice Questions",
        }

    class Media:
        css = {'all': ('/static/admin/css/widgets.css',), }
        js = ('/admin/jsi18n/',)

    def __init__(self, *args, **kwargs):
        course_id = kwargs.pop('course_id')
        print(course_id)
        # exam_paper = kwargs.pop('exam_paper')
        mcqueryset = MCQuestion.objects.filter(course_code=course_id)
        tfqueryset = TF_Question.objects.filter(course_code=course_id)
        saqueryset = SA_Question.objects.filter(course_code=course_id)
        super().__init__(*args, **kwargs)
        # self.fields['mcquestion'].required = False
        # self.fields['tfquestion'].required = False
        # self.fields['saquestion'].required = False
        # self.fields['mcquestion'].queryset = mcqueryset
        # self.fields['tfquestion'].queryset = tfqueryset
        # self.fields['saquestion'].queryset = saqueryset
        self.fields['title'] = forms.CharField(
            initial=CourseInfo.objects.get(id=course_id).Course_Name + ": Quiz " + datetime.datetime.now().strftime(
                '%D %H:%M'))

        self.fields['mcquestion'] = forms.ModelMultipleChoiceField(
            queryset=MCQuestion.objects.filter(course_code=course_id),
            required=False,
            label="Multiple Choice Questions",
            widget=FilteredSelectMultiple(verbose_name=_("MCQs"), is_stacked=False)
        )
        self.fields['saquestion'] = forms.ModelMultipleChoiceField(
            queryset=SA_Question.objects.filter(course_code=course_id),
            required=False,
            label="Short Answer Type Questions",
            widget=FilteredSelectMultiple(verbose_name=_("SAQs"), is_stacked=False)
        )
        self.fields['tfquestion'] = forms.ModelMultipleChoiceField(
            queryset=TF_Question.objects.filter(course_code=course_id),
            required=False,
            label="True/False Questions",
            widget=FilteredSelectMultiple(verbose_name=_("TFQs"), is_stacked=False)
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
        fields = ['content', 'answer_order', 'figure', 'score', 'explanation', 'course_code', 'cent_code']

    # quiz = forms.ModelMultipleChoiceField(
    #     queryset=Quiz.objects.all(),
    #     required=False,
    #     # label=_("Questions"),
    #     widget=FilteredSelectMultiple(verbose_name=_("Quizzes"), is_stacked=False))


class QuestionQuizForm(forms.ModelForm):
    class Meta:
        model = Quiz
        fields = ['mcquestion', 'tfquestion', 'saquestion']

    def __init__(self, *args, **kwargs):
        course_id = kwargs.pop('course_id', None)
        mcqueryset = MCQuestion.objects.filter(course_code=course_id)
        tfqueryset = TF_Question.objects.filter(course_code=course_id)
        saqueryset = SA_Question.objects.filter(course_code=course_id)
        super().__init__(*args, **kwargs)
        self.fields['mcquestion'] = forms.ModelMultipleChoiceField(
            queryset=mcqueryset,
            required=False,
            # label=_("Questions"),
            widget=FilteredSelectMultiple(verbose_name=_("MCQs"), is_stacked=False)
        )
        self.fields['tfquestion'] = forms.ModelMultipleChoiceField(
            queryset=tfqueryset,
            required=False,
            # label=_("Questions"),
            widget=FilteredSelectMultiple(verbose_name=_("TFQs"), is_stacked=False)
        )
        self.fields['saquestion'] = forms.ModelMultipleChoiceField(
            queryset=saqueryset,
            required=False,
            # label=_("Questions"),
            widget=FilteredSelectMultiple(verbose_name=_("SAQs"), is_stacked=False)
        )


class TFQuestionForm(forms.ModelForm):
    class Meta:
        model = TF_Question
        fields = ['correct', 'content', 'figure', 'score', 'explanation', 'course_code', 'cent_code']

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
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['correct'].widget.attrs.update({'class': 'limit_check'})


AnsFormset = inlineformset_factory(MCQuestion, Answer, form=AnswerForm, fields=['content', 'correct'], extra=2,
                                   can_delete=True)


class QuizForm1(forms.ModelForm):
    class Meta:
        model = Quiz
        fields = ['title', 'course_code', 'description']


class QuizForm2(forms.ModelForm):
    class Meta:
        model = Quiz
        fields = ['chapter_code', 'pre_test', 'post_test', 'answers_at_end', 'random_order',
                  'single_attempt', 'draft', 'exam_paper', 'duration',
                  'pass_mark', 'success_text', 'fail_text', 'negative_marking', 'negative_percentage']

    def clean(self):
        cleaned_data = super().clean()
        exam_val = cleaned_data.get("exam_paper")
        pre_val = cleaned_data.get("pre_test")
        post_val = cleaned_data.get("post_test")
        time_val = cleaned_data.get("duration")
        pass_val = cleaned_data.get("pass_mark")

        if exam_val:
            if not time_val:
                raise forms.ValidationError(
                    {
                        'duration': ["Please Enter Quiz Duration", ],
                    }
                )
            if not pass_val:
                raise forms.ValidationError(
                    {
                        'pass_mark': ["Please Enter Pass Marks", ],
                    }
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
                Column(
                    Div(css_id='test_error', css_class="text-danger"),
                    css_class='form-group col-md-12 mb-0'
                ),
                css_class='form-row'
            ),
            Row(
                Column('duration', css_class='form-group col-md-4 mb-0'),
                Column('pass_mark', css_class='form-group col-md-4 mb-0'),
                Column(css_class='form-group col-md-4 mb-0'),
                css_class='form-row'
            ),
            HTML('''<hr size="10">'''),
            HTML('''<label class=quiz-add-label>Quiz Features</label>'''),
            Row(
                Column('random_order', css_class='form-group col-md-4 mb-0'),
                Column('single_attempt', css_class='form-group col-md-4 mb-0'),
                Column('draft', css_class='form-group col-md-4 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('negative_marking', css_class='form-group col-md-6 mb-0'),
                Column('negative_percentage', css_class='form-group col-md-6 mb-0'),
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
        fields = ['mcquestion', 'tfquestion', 'saquestion', 'mcquestion_order', 
                    'saquestion_order', 'tfquestion_order']


    def __init__(self, *args, **kwargs):
        mc_queryset = kwargs.pop('mc_queryset')
        sa_queryset = kwargs.pop('sa_queryset')
        tf_queryset = kwargs.pop('tf_queryset')
        super().__init__(*args, **kwargs)
        self.fields['mcquestion'] = forms.ModelMultipleChoiceField(
            queryset=mc_queryset,
            required=False,
            label="Multiple Choice Questions",
            widget=FilteredSelectMultiple(verbose_name=_("MCQs"), is_stacked=False)
        )
        self.fields['saquestion'] = forms.ModelMultipleChoiceField(
            queryset=sa_queryset,
            required=False,
            label="Short Answer Type Questions",
            widget=FilteredSelectMultiple(verbose_name=_("SAQs"), is_stacked=False)
        )
        self.fields['tfquestion'] = forms.ModelMultipleChoiceField(
            queryset=tf_queryset,
            required=False,
            label="True/False Questions",
            widget=FilteredSelectMultiple(verbose_name=_("TFQs"), is_stacked=False)
        )
        # self.fields['mcquestion'].required = False
        # self.fields['tfquestion'].required = False
        # self.fields['saquestion'].required = False

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

    class Media:
        css = {'all': ('/static/admin/css/widgets.css',), }
        js = ('/admin/jsi18n/',)

class QuizBasicInfoForm(forms.ModelForm):
    class Meta:
        model = Quiz
        fields = ['title', 'course_code', 'description', 'chapter_code', 'pre_test', 'post_test', 'answers_at_end',
                  'random_order', 'single_attempt', 'draft', 'exam_paper', 'duration', 'pass_mark', 'success_text',
                  'fail_text', 'negative_marking', 'negative_percentage']

    def clean(self):
        cleaned_data = super().clean()
        exam_val = cleaned_data.get("exam_paper")
        pre_val = cleaned_data.get("pre_test")
        post_val = cleaned_data.get("post_test")
        time_val = cleaned_data.get("duration")
        pass_val = cleaned_data.get("pass_mark")

        if exam_val:
            if not time_val:
                raise forms.ValidationError(
                    {
                        'duration': ["Please Enter Quiz Duration", ],
                    }
                )
            if not pass_val:
                raise forms.ValidationError(
                    {
                        'pass_mark': ["Please Enter Pass Marks", ],
                    }
                )
        return cleaned_data

    def __init__(self, *args, **kwargs):
        my_obj = kwargs.pop('current_obj', None)
        super().__init__(*args, **kwargs)
        self.fields['course_code'].queryset = CourseInfo.objects.filter(Center_Code=my_obj.cent_code)
        if my_obj.exam_paper:
            # self.fields['single_attempt'].widget.attrs['class'] = "readonly-field"
            self.fields['chapter_code'].widget.attrs['class'] = "readonly-field"

        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.label_class = 'quiz-add-label'
        self.helper.layout = Layout(
            Row(
                Column('title', css_class='form-group col-md-4 mb-0'),
                Column('course_code', css_class='form-group col-md-4 mb-0'),
                Column('chapter_code', css_class='form-group col-md-4 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column(PrependedText('description', '<i class="fa fa-edit"></i>', rows='5'),
                       css_class='form-group col-md-4 mb-0'
                       ),
                Column(PrependedText('success_text', '<i class="fa fa-edit"></i>', rows='5'),
                       css_class='form-group col-md-4 mb-0'
                       ),
                Column(PrependedText('fail_text', '<i class="fa fa-edit"></i>', rows='5'),
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
                Column(
                    Div(css_id='test_error', css_class="text-danger"),
                    css_class='form-group col-md-12 mb-0'
                ),
                css_class='form-row'
            ),
            Row(
                Column('duration', css_class='form-group col-md-4 mb-0'),
                Column('pass_mark', css_class='form-group col-md-4 mb-0'),
                Column(css_class='form-group col-md-4 mb-0'),
                css_class='form-row'
            ),
            HTML('''<hr size="10">'''),
            HTML('''<label class=quiz-add-label>Quiz Features</label>'''),
            Row(
                Column('negative_marking', css_class='form-group col-md-3 mb-0'),
                Column('random_order', css_class='form-group col-md-3 mb-0'),
                Column('single_attempt', css_class='form-group col-md-3 mb-0'),
                Column('draft', css_class='form-group col-md-3 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('negative_percentage', css_class='form-group col-md-12 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column(css_class='col-md-4 mb-0'),
                Column(css_class='col-md-4 mb-0'),
                Column(
                    StrictButton('Save', css_class='add-mcq', type='submit'),
                    css_class='col-md-4 mb-0 text-right'
                ),
                css_class='form-row'
            ),
        )

### changing order of choices acc to order field ############# 

class QuestionIterator(ModelChoiceIterator):
    def __init__(self, field, qn_order):
        self.qn_order = qn_order
        super().__init__(field)

    def __iter__(self):
        if not self.qn_order:
            if self.field.empty_label is not None:
                yield ("", self.field.empty_label)
            queryset = self.queryset
            # Can't use iterator() when queryset uses prefetch_related()
            if not queryset._prefetch_related_lookups:
                queryset = queryset.iterator()
            for obj in queryset:
                yield self.choice(obj)
        else:
            qs = self.queryset
            qn_order = self.qn_order
            # if qn_order:
            #     qn_order = [int(x) for x in qn_order.split(",")]
            # else:
            #     qn_order = []
            qn_o_pk = [x.pk for x in qn_order]
            qs_unselected = qs.exclude(pk__in=qn_o_pk)
            tp_unselected_list = []
            tp_selected_list = []
            for q in qs_unselected:
                tp_unselected_list.append((q.pk, q.content))
            for q in qn_order:
                # q = MCQuestion.objects.get(pk=q_pk)
                tp_selected_list.append((q.pk, q.content))
            for q_tp in tp_selected_list + tp_unselected_list:
                yield q_tp 

class QuestionField(forms.ModelMultipleChoiceField):
    def __init__(self, *args, qn_order, **kwargs):
        self.iterator = partial(QuestionIterator, qn_order=qn_order)
        super().__init__(*args, **kwargs)

class ChooseMCQForm(forms.ModelForm):
    class Meta:
        model = Quiz
        fields = ['mcquestion', 'mcquestion_order']

    class Media:
        css = {'all': ('/static/admin/css/widgets.css',), }
        js = ('/admin/jsi18n/',)

    def __init__(self, *args, **kwargs):
        my_obj = kwargs.pop('current_obj', None)
        qn_pk_str = my_obj.mcquestion_order if my_obj else None
        qn_order=[]
        if qn_pk_str:
            for x in qn_pk_str.split(","):
                qn_order.append(MCQuestion.objects.get(pk=int(x)))
        print("MCQ quiz object: ", my_obj)
        super().__init__(*args, **kwargs)
        self.fields['mcquestion'] = QuestionField(
            queryset=MCQuestion.objects.filter(course_code=my_obj.course_code),
            required=False,
            widget=FilteredSelectMultiple(verbose_name=_("MCQs"), is_stacked=False),
            qn_order=qn_order,
        )
        self.fields['mcquestion_order'].widget = forms.HiddenInput()


    def clean(self):
        cleaned_data = super().clean()
        mq = cleaned_data.get("mcquestion")
        if not mq or len(mq) == 0:
            if not (self.instance.has_saqs() or self.instance.has_tfqs()):
                raise forms.ValidationError(
                    "Quiz must have atleast one question.", code=500
                )
        return cleaned_data

class ChooseTFQForm(forms.ModelForm):
    class Meta:
        model = Quiz
        fields = ['tfquestion', 'tfquestion_order']

    class Media:
        css = {'all': ('/static/admin/css/widgets.css',), }
        js = ('/admin/jsi18n/',)

    def __init__(self, *args, **kwargs):
        my_obj = kwargs.pop('current_obj', None)
        qn_pk_str = my_obj.tfquestion_order if my_obj else None
        qn_order=[]
        if qn_pk_str:
            for x in qn_pk_str.split(","):
                qn_order.append(TF_Question.objects.get(pk=int(x)))
        super().__init__(*args, **kwargs)
        self.fields['tfquestion'] = QuestionField(
            queryset=TF_Question.objects.filter(course_code=my_obj.course_code),
            required=False,
            widget=FilteredSelectMultiple(verbose_name=_("TFQs"), is_stacked=False),
            qn_order=qn_order
        )
        self.fields['tfquestion_order'].widget = forms.HiddenInput()

    def clean(self):
        cleaned_data = super().clean()
        tf = cleaned_data.get("tfquestion")
        if not tf or len(tf) == 0:
            if not (self.instance.has_saqs() or self.instance.has_mcqs()):
                raise forms.ValidationError(
                    "Quiz must have atleast one question.", code=500
                )
        return cleaned_data

class ChooseSAQForm(forms.ModelForm):
    class Meta:
        model = Quiz
        fields = ['saquestion', 'saquestion_order']

    class Media:
        css = {'all': ('/static/admin/css/widgets.css',), }
        js = ('/admin/jsi18n/',)

    def __init__(self, *args, **kwargs):
        my_obj = kwargs.pop('current_obj', None)
        qn_pk_str = my_obj.saquestion_order if my_obj else None
        qn_order=[]
        if qn_pk_str:
            for x in qn_pk_str.split(","):
                qn_order.append(SA_Question.objects.get(pk=int(x)))
        super().__init__(*args, **kwargs)
        self.fields['saquestion'] = QuestionField(
            queryset=SA_Question.objects.filter(course_code=my_obj.course_code),
            required=False,
            widget=FilteredSelectMultiple(verbose_name=_("SAQs"), is_stacked=False),
            qn_order=qn_order
        )
        self.fields['saquestion_order'].widget = forms.HiddenInput()

    def clean(self):
        cleaned_data = super().clean()
        sa = cleaned_data.get("saquestion")
        if not sa or len(sa) == 0:
            if not (self.instance.has_tfqs() or self.instance.has_mcqs()):
                raise forms.ValidationError(
                    "Quiz must have atleast one question.", code=500
                )
        return cleaned_data
