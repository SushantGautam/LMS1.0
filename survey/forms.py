from datetime import timedelta, datetime

from django import forms
from django.contrib.admin.widgets import AdminTimeWidget
from django.utils import timezone

from WebApp.models import CourseInfo, InningInfo, InningGroup
from .models import CategoryInfo, SurveyInfo, QuestionInfo, OptionInfo, SubmitSurvey, AnswerInfo


class CategoryInfoForm(forms.ModelForm):
    class Meta:
        model = CategoryInfo
        fields = '__all__'


class SurveyInfoForm(forms.ModelForm):
    Start_Date = forms.CharField()
    End_Date = forms.CharField()
    End_Time = forms.DurationField()

    class Meta:
        model = SurveyInfo
        fields = ['Survey_Title', 'Category_Code', 'Start_Date', 'End_Date', 'Use_Flag', 'Publish_Result',
                  'Session_Code', 'Course_Code']

    # To filter out only active session and course of the center
    def __init__(self, *args, **kwargs):
        request = kwargs.pop("request", None)
        survey_object = kwargs.pop("object", None)
        super(SurveyInfoForm, self).__init__(*args, **kwargs)
        self.fields['Use_Flag'].label = 'Publish'
        self.fields['Use_Flag'].widget.attrs['style'] = "margin-top:30px"
        # self.fields['Use_Flag'].widget.attrs['style'] = "text-align:left"
        # self.fields['Publish_Result'].widget.attrs['style'] = "text-align:left"

        self.fields['Publish_Result'].label = 'Display Result'
        self.fields['Publish_Result'].label = 'Display Result'

        if survey_object:
            print(survey_object, "survey_obj")
            print(survey_object.Course_Code, "survey_course")
            self.fields['Session_Code'].initial = survey_object.Session_Code if survey_object.Session_Code else None
            self.fields['Course_Code'].initial = survey_object.Course_Code if survey_object.Course_Code else None

        category_name = request.GET["category_name"].lower()
        self.fields['Start_Date'].initial = timezone.now()
        self.fields['End_Date'].initial = timezone.now() + timedelta(days=30)
        self.fields['Category_Code'].widget = forms.HiddenInput()
        # self.fields['Use_Flag'].widget = forms.HiddenInput()
        self.fields['End_Time'].initial = int(timedelta(hours=6, minutes=30).total_seconds())
        self.fields['Survey_Title'].initial = "Survey " + datetime.now().strftime('%D %H:%M')

        if category_name == "live":
            self.fields['Start_Date'].widget = forms.HiddenInput()
            self.fields['End_Date'].widget = forms.HiddenInput()
            self.fields['Session_Code'].widget = forms.HiddenInput()
            self.fields['Course_Code'].widget = forms.HiddenInput()
            self.fields['Category_Code'].initial = CategoryInfo.objects.get(
                Category_Name__iexact="course"
            ).id
        elif category_name == "general":
            self.fields['Session_Code'].widget = forms.HiddenInput()
            self.fields['Course_Code'].widget = forms.HiddenInput()
            self.fields['Category_Code'].initial = CategoryInfo.objects.get(
                Category_Name__iexact=category_name
            ).id
            self.fields['End_Time'].widget = forms.HiddenInput()
        elif category_name == "session":
            self.fields['Course_Code'].widget = forms.HiddenInput()
            self.fields['Session_Code'].required = True
            self.fields['Category_Code'].initial = CategoryInfo.objects.get(
                Category_Name__iexact=category_name
            ).id
            self.fields['End_Time'].widget = forms.HiddenInput()
        elif category_name == "course":
            self.fields['Session_Code'].widget = forms.HiddenInput()
            self.fields['Course_Code'].required = True
            self.fields['Category_Code'].initial = CategoryInfo.objects.get(
                Category_Name__iexact=category_name
            ).id
            self.fields['End_Time'].widget = forms.HiddenInput()
        elif category_name == "system":
            self.fields['Session_Code'].widget = forms.HiddenInput()
            self.fields['Course_Code'].widget = forms.HiddenInput()
            self.fields['Category_Code'].initial = CategoryInfo.objects.get(
                Category_Name__iexact=category_name
            ).id
            self.fields['End_Time'].widget = forms.HiddenInput()
        else:
            self.fields['Category_Code'].initial = CategoryInfo.objects.get(
                Category_Name__iexact=category_name
            ).id
            self.fields['End_Time'].widget = forms.HiddenInput()

        if "teachers" in request.path:
            print(request.path)
            innings_Course_Code = InningGroup.objects.filter(Teacher_Code=request.user.id).values('Course_Code')
            self.fields['Course_Code'].queryset = CourseInfo.objects.filter(
                Center_Code=request.user.Center_Code,
                Use_Flag=True,
                id__in=innings_Course_Code,
            )
            self.fields['Session_Code'].queryset = InningInfo.objects.filter(
                Course_Group__in=InningGroup.objects.filter(Teacher_Code=request.user.id)
            ).distinct()
        else:
            self.fields['Course_Code'].queryset = CourseInfo.objects.filter(Center_Code=request.user.Center_Code,
                                                                            Use_Flag=True)
            self.fields['Session_Code'].queryset = InningInfo.objects.filter(Use_Flag=True,
                                                                             Center_Code=request.user.Center_Code)

    #     Id = kwargs["categoryId"]
    #     if Id == 'live':
    #         self.fields['End_Date'].widget = widgets.AdminTimeWidget()
    #     else:
    #         self.fields['Start_Date'].widget = widgets.AdminDateWidget()
    #         self.fields['End_Date'].widget = widgets.AdminDateWidget()


class SurveyInfoFormUpdateLimited(forms.ModelForm):
    # Start_Date = forms.DateTimeField(widget=forms.DateInput(attrs={'type': 'date', 'max': '9999-12-31'}))
    End_Date = forms.CharField()
    End_Time = forms.DurationField()

    class Meta:
        model = SurveyInfo
        fields = ['Survey_Title', 'End_Date', 'Use_Flag', 'Publish_Result', ]

    def __init__(self, *args, **kwargs):
        request = kwargs.pop("request", None)
        survey_object = kwargs.pop("object", None)
        super().__init__(*args, **kwargs)
        self.fields['Use_Flag'].label = 'Publish'
        self.fields['Publish_Result'].label = 'Display Result'

        category_name = request.GET["category_name"].lower()
        if category_name == "live" or category_name == "course":
            self.fields['End_Time'].initial = int((survey_object.End_Date - survey_object.Start_Date).total_seconds())
            self.fields['End_Date'].widget = forms.HiddenInput()
        else:
            self.fields['End_Time'].widget = forms.HiddenInput()
            self.fields['End_Time'].required = False


class LiveSurveyInfoForm(forms.ModelForm):
    # End_Date = forms.DateTimeField(label='End Time', widget=forms.DateInput(attrs={'type': 'time'}))
    End_Time = forms.TimeField()

    class Meta:
        model = SurveyInfo
        fields = ['Survey_Title', ]
        help_texts = {
            'End_Time': 'Survey Duration',
        }

    # To filter out only active session and course of the center
    def __init__(self, *args, **kwargs):
        request = kwargs.pop("request", None)
        super(LiveSurveyInfoForm, self).__init__(*args, **kwargs)
        self.fields['End_Time'].widget = AdminTimeWidget()
        # self.fields['Session_Code'].queryset = InningInfo.objects.filter(Use_Flag=True,
        #                                                                  Center_Code=request.user.Center_Code)
        # self.fields['Course_Code'].queryset = CourseInfo.objects.filter(Center_Code=request.user.Center_Code,
        #                                                                 Use_Flag=True)


class QuestionInfoForm(forms.ModelForm):
    class Meta:
        model = QuestionInfo
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(QuestionInfoForm, self).__init__(*args, **kwargs)
        self.fields['Question_Name'].widget.attrs['placeholder'] = "Add Question"
        self.fields['Question_Name'].label = ""


class OptionInfoForm(forms.ModelForm):
    class Meta:
        model = OptionInfo
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(OptionInfoForm, self).__init__(*args, **kwargs)
        self.fields['Option_Name'].widget.attrs['placeholder'] = "Add Option"
        self.fields['Option_Name'].label = ""


class SubmitSurveyForm(forms.ModelForm):
    class Meta:
        model = SubmitSurvey
        fields = '__all__'


class AnswerInfoForm(forms.ModelForm):
    class Meta:
        model = AnswerInfo
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(AnswerInfoForm, self).__init__(*args, **kwargs)
        OptionInfoForm.fields['Option_Name'].label = ""
        QuestionInfoForm.fields['Question_Name'].label = ""


# fields=('Question_Name', 'Question_Type', 'Survey_Code'))

from django.forms.models import inlineformset_factory, BaseInlineFormSet

OptionInfoFormset = inlineformset_factory(
    QuestionInfo,
    OptionInfo,
    fields=('Option_Name',),
    can_delete=False,
    extra=0,
    form=OptionInfoForm,
)

AnswerInfoFormset = inlineformset_factory(
    QuestionInfo,
    AnswerInfo,
    fields=('Answer_Value',),
    extra=1,
    # form=AnswerInfoForm,

)


class BaseQuestionInfoFormset(BaseInlineFormSet):
    def add_fields(self, form, index):
        super().add_fields(form, index)

        # if not form.is_bound:
        #     form.fields['Question_Name'].initial = "hello"

        # save the formset in the 'nested' property
        form.fields['Question_Type'].initial = "MCQ"
        form.fields['Question_Type'].widget = forms.HiddenInput()
        form.nested = OptionInfoFormset(
            instance=form.instance,
            data=form.data if form.is_bound else None,
            files=form.files if form.is_bound else None,
            prefix='optioninfo-%s-%s' % (
                form.prefix,
                OptionInfoFormset.get_default_prefix()),
        )

    def is_valid(self):
        result = super().is_valid()

        if self.is_bound:
            for form in self.forms:
                if hasattr(form, 'nested'):
                    result = result and form.nested.is_valid()

        return result

    def save(self, commit=True):

        result = super().save(commit=commit)

        for form in self.forms:
            if hasattr(form, 'nested'):
                if not self._should_delete_form(form):
                    form.nested.save(commit=commit)

        return result


class BaseQuestionAnsInfoFormset(BaseInlineFormSet):

    def add_fields(self, form, index):
        super().add_fields(form, index)

        # save the formset in the 'nested' property
        form.nested = AnswerInfoFormset(
            instance=form.instance,
            data=form.data if form.is_bound else None,
            files=form.files if form.is_bound else None,
            prefix='answerinfo-%s-%s' % (
                form.prefix,
                OptionInfoFormset.get_default_prefix()),
        )

    def is_valid(self):
        result = super().is_valid()

        if self.is_bound:
            for form in self.forms:
                if hasattr(form, 'nested'):
                    result = result and form.nested.is_valid()

        return result

    def save(self, commit=True):

        result = super().save(commit=commit)

        for form in self.forms:
            if hasattr(form, 'nested'):
                if not self._should_delete_form(form):
                    form.nested.save(commit=commit)

        return result


QuestionInfoFormset = inlineformset_factory(
    SurveyInfo,
    QuestionInfo,
    formset=BaseQuestionInfoFormset,
    form=QuestionInfoForm,
    fields=('Question_Name', 'Question_Type'),
    extra=1,
    can_delete=False,
)

QuestionAnsInfoFormset = inlineformset_factory(
    SurveyInfo,
    QuestionInfo,
    form=QuestionInfoForm,
    fields=('Question_Name', 'Question_Type'),
    extra=1,
    can_delete=False,
)
