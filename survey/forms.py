from django import forms
from .models import CategoryInfo, SurveyInfo, QuestionInfo, OptionInfo, SubmitSurvey, AnswerInfo
from WebApp.models import MemberInfo, CenterInfo


class CategoryInfoForm(forms.ModelForm):
    class Meta:
        model = CategoryInfo
        fields = '__all__'


class SurveyInfoForm(forms.ModelForm):
    class Meta:
        model = SurveyInfo
        fields = '__all__'


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
from django.forms import modelformset_factory, BaseModelFormSet

OptionInfoFormset = inlineformset_factory(
    QuestionInfo,
    OptionInfo,
    fields=('Option_Name',),
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
    )

QuestionAnsInfoFormset = inlineformset_factory(
    SurveyInfo,
    QuestionInfo, 
    formset = BaseQuestionAnsInfoFormset,
    fields=('Question_Name', 'Question_Type'),
    extra=1,
    )