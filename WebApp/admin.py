from django import forms
from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from import_export.admin import ImportExportModelAdmin, ExportMixin
from import_export.resources import ModelResource

from .models import CenterInfo, MemberInfo, SessionInfo, InningInfo, InningGroup, GroupMapping, MessageInfo, \
    CourseInfo, ChapterInfo, AssignmentInfo, AssignmentQuestionInfo, AssignAssignmentInfo, AssignAnswerInfo, \
    InningManager, Attendance, Notice, NoticeView


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

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)

        if user.id is None:
            user.set_password(self.cleaned_data["password"])
        else:
            if MemberInfo.objects.get(id=user.id).password != user.password:
                user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()

        return user


class MemberInfoResource(ModelResource):
    class Meta:
        model = MemberInfo
        fields = ['id', 'username', 'password', 'first_name', 'last_name', 'email', 'Center_Code',
                  'Member_Permanent_Address',
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
    search_fields = ('username',)


admin.site.register(MemberInfo, MemberInfoAdmin)


class CourseInfoAdminForm(forms.ModelForm):
    class Meta:
        model = CourseInfo
        fields = '__all__'


class CourseInfoAdmin(admin.ModelAdmin):
    form = CourseInfoAdminForm
    list_display = ['id', 'Course_Name', 'Course_Cover_File', 'Course_Level',
                    'Course_Info', 'Use_Flag', 'Register_DateTime', 'Updated_DateTime', 'Register_Agent',
                    'Course_Provider', 'Center_Code']
    search_fields = ('Course_Name',)


admin.site.register(CourseInfo, CourseInfoAdmin)


class ChapterInfoResource(ModelResource):
    class Meta:
        model = ChapterInfo

    def dehydrate_Register_DateTime(self, chapter):
        return chapter.Register_DateTime.strftime("%Y-%m-%d")

    def dehydrate_Updated_DateTime(self, chapter):
        return chapter.Register_DateTime.strftime("%Y-%m-%d")

    def dehydrate_Course_Code(self, chapter):
        return chapter.Course_Code.Course_Name


class ChapterInfoAdminForm(forms.ModelForm):
    class Meta:
        model = ChapterInfo
        fields = '__all__'


class ChapterInfoAdmin(ExportMixin, admin.ModelAdmin):
    resource_class = ChapterInfoResource
    form = ChapterInfoAdminForm
    list_display = ['id', 'Chapter_No', 'Chapter_Name', 'Summary', 'Page_Num', 'Use_Flag', 'mustreadtime',
                    'Register_DateTime', 'Updated_DateTime', 'Register_Agent', 'Course_Code']
    search_fields = ('Chapter_Name',)
    list_filter = ('Course_Code',)


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
        model = AssignmentQuestionInfo
        fields = '__all__'


class QuestionInfoAdmin(admin.ModelAdmin):
    form = QuestionInfoAdminForm
    list_display = ['Question_Title', 'Question_Score', 'Use_Flag', 'Register_DateTime', 'Updated_DateTime',
                    'Register_Agent', 'Question_Media_File', 'Question_Description', 'Assignment_Code',
                    'Answer_Choices', 'Answer_Type']


admin.site.register(AssignmentQuestionInfo, QuestionInfoAdmin)


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


class InningManagerAdmin(admin.ModelAdmin):
    list_display = ["sessioninfoobj", ]


admin.site.register(InningManager, InningManagerAdmin)


class AttendanceAdminForm(forms.ModelForm):
    class Meta:
        model = Attendance
        fields = '__all__'


class AttendanceAdmin(admin.ModelAdmin):
    form = AttendanceAdminForm
    list_display = ['attendance_date', 'present']
    readonly_fields = ['attendance_date', 'present']


admin.site.register(Attendance, AttendanceAdmin)


class NoticeAdmin(SummernoteModelAdmin):
    list_display = ['title', 'status', 'show', 'Start_Date', 'End_Date']
    summernote_fields = ('message',)


admin.site.register(Notice, NoticeAdmin)


class NoticeViewAdmin(admin.ModelAdmin):
    list_display = ['user_code', 'notice_code', 'dont_show']


admin.site.register(NoticeView, NoticeViewAdmin)
