from django import forms

from .models import CategoryInfo, SurveyInfo, QuestionInfo, OptionInfo, SubmitSurvey, AnswerInfo
from WebApp.models import CourseInfo, InningInfo


class CategoryInfoForm(forms.ModelForm):
    class Meta:
        model = CategoryInfo
        fields = '__all__'


class SurveyInfoForm(forms.ModelForm):
    Start_Date = forms.DateTimeField(widget=forms.DateInput(attrs={'type': 'date'}))
    End_Date = forms.DateTimeField(widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = SurveyInfo
        fields = ['Survey_Title', 'Category_Code', 'Start_Date', 'End_Date',
                  'Session_Code', 'Course_Code']

    # To filter out only active session and course of the center
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        super(SurveyInfoForm, self).__init__(*args, **kwargs)
        self.fields['Session_Code'].queryset = InningInfo.objects.filter(Use_Flag=True,
                                                                          Center_Code=self.request.user.Center_Code)
        self.fields['Course_Code'].queryset = CourseInfo.objects.filter(Center_Code=self.request.user.Center_Code,
                                                                         Use_Flag=True)
    #     Id = kwargs["categoryId"]
    #     if Id == 'live':
    #         self.fields['End_Date'].widget = widgets.AdminTimeWidget()
    #     else:
    #         self.fields['Start_Date'].widget = widgets.AdminDateWidget()
    #         self.fields['End_Date'].widget = widgets.AdminDateWidget()


class LiveSurveyInfoForm(forms.ModelForm):
    # End_Date = forms.DateTimeField(label='End Time', widget=forms.DateInput(attrs={'type': 'time'}))

    class Meta:
        model = SurveyInfo
        fields = ['Survey_Title', 'Category_Code',
                  'Session_Code', 'Course_Code']
        # labels = {'End_Date': 'End Time',}
        # setattr()


class QuestionInfoForm(forms.ModelForm):
    class Meta:
        model = QuestionInfo
        fields = '__all__'


class OptionInfoForm(forms.ModelForm):
    class Meta:
        model = OptionInfo
        fields = '__all__'


class SubmitSurveyForm(forms.ModelForm):
    class Meta:
        model = SubmitSurvey
        fields = '__all__'


class AnswerInfoForm(forms.ModelForm):
    class Meta:
        model = AnswerInfo
        fields = '__all__'

#fields=('Question_Name', 'Question_Type', 'Survey_Code'))

from django.forms.models import inlineformset_factory, BaseInlineFormSet

OptionInfoFormset = inlineformset_factory(
    QuestionInfo,
    OptionInfo,
    fields=('Option_Name',),
    can_delete=False,
    extra=1,
)

AnswerInfoFormset = inlineformset_factory(
    QuestionInfo,
    AnswerInfo,
    fields=('Answer_Value',),
    extra=1,
)

class BaseQuestionInfoFormset(BaseInlineFormSet):
    def add_fields(self, form, index):
        super().add_fields(form, index)

        # save the formset in the 'nested' property
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
    formset = BaseQuestionInfoFormset,
    fields=('Question_Name', 'Question_Type'),
    extra=1,
    can_delete=False,
)

QuestionAnsInfoFormset = inlineformset_factory(
    SurveyInfo,
    QuestionInfo, 
    form = QuestionInfoForm,
    fields=('Question_Name', 'Question_Type'),
    extra=1,
    can_delete=False,
)
