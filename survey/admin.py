from django.contrib import admin
from django import forms
from .models import CategoryInfo, SurveyInfo, QuestionInfo, OptionInfo, SubmitSurvey, AnswerInfo
from WebApp.models import MemberInfo, CenterInfo


class CategoryInfoAdminForm(forms.ModelForm):

    class Meta:
        model = CategoryInfo
        fields = '__all__'


class CategoryInfoAdmin(admin.ModelAdmin):
    form = CategoryInfoAdminForm
    list_display = ['Category_Name', 'Category_Icon']
    # readonly_fields = ['Category_Name']


admin.site.register(CategoryInfo, CategoryInfoAdmin)


class SurveyInfoAdminForm(forms.ModelForm):

    class Meta:
        model = SurveyInfo
        fields = '__all__'


class SurveyInfoAdmin(admin.ModelAdmin):
    form = SurveyInfoAdminForm
    list_display = ['Survey_Title', 'Start_Date', 'End_Date', 'Survey_Cover',
                    'Use_Flag', 'Added_By', 'Category_Code', 'Session_Code', 'Course_Code', 'Center_Code']
    # readonly_fields = ['Survey_Title', 'Start_Date', 'End_Date', 'Survey_Cover', 'Use_Flag']


admin.site.register(SurveyInfo, SurveyInfoAdmin)


class QuestionInfoAdminForm(forms.ModelForm):

    class Meta:
        model = QuestionInfo
        fields = '__all__'


class QuestionInfoAdmin(admin.ModelAdmin):
    form = QuestionInfoAdminForm
    list_display = ['Question_Name', 'Survey_Code', 'Question_Type']
    # readonly_fields = ['Question_Name']


admin.site.register(QuestionInfo, QuestionInfoAdmin)


class OptionInfoAdminForm(forms.ModelForm):

    class Meta:
        model = OptionInfo
        fields = '__all__'


class OptionInfoAdmin(admin.ModelAdmin):
    form = OptionInfoAdminForm
    list_display = ['Option_Name', 'Question_Code']
    # readonly_fields = ['Option_Name']


admin.site.register(OptionInfo, OptionInfoAdmin)


class SubmitSurveyAdminForm(forms.ModelForm):

    class Meta:
        model = SubmitSurvey
        fields = '__all__'


class SubmitSurveyAdmin(admin.ModelAdmin):
    form = SubmitSurveyAdminForm
    list_display = ['Survey_Code', 'Student_Code']


admin.site.register(SubmitSurvey, SubmitSurveyAdmin)


class AnswerInfoAdminForm(forms.ModelForm):

    class Meta:
        model = AnswerInfo
        fields = '__all__'


class AnswerInfoAdmin(admin.ModelAdmin):
    form = AnswerInfoAdminForm
    list_display = ['Answer_Value', 'Question_Code', 'Submit_Code']
    # readonly_fields = ['Answer_Value']


admin.site.register(AnswerInfo, AnswerInfoAdmin)
