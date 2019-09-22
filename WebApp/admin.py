from django import forms
from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from import_export.resources import ModelResource

from .models import CenterInfo, MemberInfo, SessionInfo, InningInfo, InningGroup, GroupMapping, MessageInfo, \
    CourseInfo, ChapterInfo, AssignmentInfo, QuestionInfo, AssignAssignmentInfo, AssignAnswerInfo


class CenterInfoAdminForm(forms.ModelForm):
    class Meta:
        model = CenterInfo
        fields = '__all__'


class CenterInfoAdmin(admin.ModelAdmin):
    form = CenterInfoAdminForm
    list_display = ['Center_Name', 'Center_Address', 'Use_Flag', 'Register_DateTime', 'Register_Agent']


admin.site.register(CenterInfo, CenterInfoAdmin)


class MemberInfoAdminForm(forms.ModelForm):
    class Meta:
        model = MemberInfo
        fields = '__all__'


class MemberInfoResource(ModelResource):
    class Meta:
        model = MemberInfo
        fields = ['id', 'username', 'password', 'first_name', 'last_name', 'email', 'Member_Permanent_Address',
                  'Member_Temporary_Address', 'Member_BirthDate', 'Member_Phone', 'Member_Avatar',
                  'Member_Gender', 'Use_Flag', 'Register_DateTime', 'Updated_DateTime', 'Register_Agent',
                  'Member_Memo', 'Member_ID', 'Is_Teacher', 'Is_Student', ]


class MemberInfoAdmin(ImportExportModelAdmin):
    resource_class = MemberInfoResource
    form = MemberInfoAdminForm
    list_display = ['id', 'username', 'first_name', 'last_name', 'email', 'Member_Permanent_Address',
                    'Member_Temporary_Address', 'Member_BirthDate', 'Member_Phone', 'Member_Avatar',
                    'Member_Gender', 'Use_Flag', 'Register_DateTime', 'Updated_DateTime', 'Register_Agent',
                    'Member_Memo']
    list_display_links = ['id', 'username']


admin.site.register(MemberInfo, MemberInfoAdmin)


class CourseInfoAdminForm(forms.ModelForm):
    class Meta:
        model = CourseInfo
        fields = '__all__'


class CourseInfoAdmin(admin.ModelAdmin):
    form = CourseInfoAdminForm
    list_display = ['Course_Name', 'Course_Cover_File', 'Course_Level',
                    'Course_Info', 'Use_Flag', 'Register_DateTime', 'Updated_DateTime', 'Register_Agent',
                    'Course_Provider', 'Center_Code']


admin.site.register(CourseInfo, CourseInfoAdmin)


class ChapterInfoAdminForm(forms.ModelForm):
    class Meta:
        model = ChapterInfo
        fields = '__all__'


class ChapterInfoAdmin(admin.ModelAdmin):
    form = ChapterInfoAdminForm
    list_display = ['Chapter_No', 'Chapter_Name', 'Summary', 'Page_Num', 'Use_Flag',
                    'Register_DateTime', 'Updated_DateTime', 'Register_Agent', 'Course_Code']


admin.site.register(ChapterInfo, ChapterInfoAdmin)


# AssignmentInfoModels
class AssignmentInfoAdminForm(forms.ModelForm):
    class Meta:
        model = AssignmentInfo
        fields = '__all__'


class AssignmentInfoAdmin(admin.ModelAdmin):
    form = AssignmentInfoAdminForm
    list_display = ['Course_Code', 'Chapter_Code', 'Assignment_Topic', 'Use_Flag', 'Register_DateTime',
                    'Updated_DateTime', 'Assignment_Deadline', 'Register_Agent']


admin.site.register(AssignmentInfo, AssignmentInfoAdmin)


class QuestionInfoAdminForm(forms.ModelForm):
    class Meta:
        model = QuestionInfo
        fields = '__all__'


class QuestionInfoAdmin(admin.ModelAdmin):
    form = QuestionInfoAdminForm
    list_display = ['Question_Title', 'Question_Score', 'Use_Flag', 'Register_DateTime', 'Updated_DateTime',
                    'Register_Agent', 'Question_Media_File', 'Question_Description', 'Assignment_Code',
                    'Answer_Choices', 'Answer_Type']


admin.site.register(QuestionInfo, QuestionInfoAdmin)


class AssignAssignmentInfoAdminForm(forms.ModelForm):
    class Meta:
        model = AssignAssignmentInfo
        fields = '__all__'


class AssignAssignmentInfoAdmin(admin.ModelAdmin):
    form = AssignAssignmentInfoAdminForm
    list_display = ['Use_Flag', 'Register_DateTime', 'Updated_DateTime', 'Inning_Code', 'Assignment_Code',
                    'Assigned_By']


admin.site.register(AssignAssignmentInfo, AssignAssignmentInfoAdmin)


class AssignAnswerInfoAdminForm(forms.ModelForm):
    class Meta:
        model = AssignAnswerInfo
        fields = '__all__'


class AssignAnswerInfoAdmin(admin.ModelAdmin):
    form = AssignAnswerInfoAdminForm
    list_display = ['Assignment_Score', 'Question_Code',
                    'Use_Flag', 'Register_DateTime', 'Updated_DateTime', 'Assignment_Answer', 'Student_Code']


admin.site.register(AssignAnswerInfo, AssignAnswerInfoAdmin)


class SessionInfoAdminForm(forms.ModelForm):
    class Meta:
        model = SessionInfo
        fields = '__all__'


class SessionInfoAdmin(admin.ModelAdmin):
    form = SessionInfoAdminForm
    list_display = ['Session_Name', 'Description', 'Use_Flag', 'Center_Code']
    # readonly_fields = ['inning_name', 'start_date', 'end_date', 'Use_Flag', 'Register_DateTime', 'Updated_DateTime', 'Register_Agent']


admin.site.register(SessionInfo, SessionInfoAdmin)


class InningGroupAdminForm(forms.ModelForm):
    class Meta:
        model = InningGroup
        fields = '__all__'


class InningGroupAdmin(admin.ModelAdmin):
    form = InningGroupAdminForm
    list_display = ['Course_Code', 'Center_Code', 'Use_Flag', 'Register_DateTime',
                    'Updated_DateTime', 'Register_Agent']
    # readonly_fields = ['teacher_code', 'Use_Flag', 'Register_DateTime', 'Updated_DateTime', 'Register_Agent']


admin.site.register(InningGroup, InningGroupAdmin)


class InningInfoAdminForm(forms.ModelForm):
    class Meta:
        model = InningInfo
        fields = '__all__'


class InningInfoAdmin(admin.ModelAdmin):
    form = InningInfoAdminForm
    list_display = ['Inning_Name', 'Start_Date', 'End_Date', 'Use_Flag', 'Register_DateTime',
                    'Updated_DateTime',
                    'Register_Agent', 'Center_Code', 'Groups']
    # readonly_fields = ['inning_name', 'start_date', 'end_date', 'Use_Flag', 'Register_DateTime', 'Updated_DateTime', 'Register_Agent']


admin.site.register(InningInfo, InningInfoAdmin)


class GroupMappingAdminForm(forms.ModelForm):
    class Meta:
        model = GroupMapping
        fields = '__all__'


class GroupMappingAdmin(admin.ModelAdmin):
    form = GroupMappingAdminForm
    list_display = ['GroupMapping_Name', 'Use_Flag', 'Register_DateTime', 'Updated_DateTime',
                    'Register_Agent', 'Center_Code']
    # readonly_fields = ['use_flag', 'reg_date', 'reg_time', 'reg_agent', 'udt_date', 'udt_time', 'udt_agent']


admin.site.register(GroupMapping, GroupMappingAdmin)


class MessageInfoAdminForm(forms.ModelForm):
    class Meta:
        model = MessageInfo
        fields = '__all__'


class MessageInfoAdmin(admin.ModelAdmin):
    form = MessageInfoAdminForm
    list_display = ['teacher_code', 'message', 'message_read', 'Use_Flag', 'Register_DateTime', 'Updated_DateTime',
                    'Register_Agent']
    # readonly_fields = ['teacher_code', 'message', 'message_read', 'Use_Flag', 'Register_DateTime', 'Updated_DateTime', 'Register_Agent']


admin.site.register(MessageInfo, MessageInfoAdmin)
