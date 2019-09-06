from django import forms
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm, TextInput

from .models import CenterInfo, MemberInfo, SessionInfo, InningInfo, InningGroup, GroupMapping, MessageInfo, \
                    CourseInfo, ChapterInfo, AssignmentInfo, QuestionInfo, AssignAssignmentInfo, AssignAnswerInfo, USER_ROLES


class UserRegisterForm(UserCreationForm):
    # Member_Role = forms.MultipleChoiceField(choices=USER_ROLES, widget=forms.CheckboxSelectMultiple())

    class Meta(UserCreationForm.Meta):
        model = MemberInfo
        fields = ('username', 'email', 'Member_Gender', 'Center_Code', 'Is_Student', 'Is_Teacher','Use_Flag')


class UserUpdateForm(forms.ModelForm):
    role = forms.MultipleChoiceField(choices=USER_ROLES, )

    class Meta:
        model = MemberInfo
        fields = ('username', 'email')
        widgets = {
            'role': forms.CheckboxSelectMultiple,
        }


class UserUpdateFormForAdmin(forms.ModelForm):
    class Meta:
        model = MemberInfo
        fields = '__all__'


class CenterInfoForm(forms.ModelForm):
    class Meta:
        model = CenterInfo
        fields = ['Center_Name', 'Center_Address', 'Use_Flag', 'Register_Agent']


class MemberInfoForm(forms.ModelForm):
    class Meta:
        model = MemberInfo
        # fields = 'username', 'first_name', 'last_name', 'email', 'date_joined', 'Member_Permanent_Address', 'Member_Temporary_Address', 'Member_BirthDate', 'Member_Phone', 'Member_Avatar', 'Member_Gender', 'Member_Memo','Center_Code'
        fields = '__all__'
        exclude = ('last_login', 'date_joined', 'password', 'is_staff', 'is_active', 'is_superuser')


class CourseInfoForm(forms.ModelForm):
    class Meta:
        model = CourseInfo
        fields = '__all__'


class ChapterInfoForm(forms.ModelForm):
    class Meta:
        model = ChapterInfo
        fields = '__all__'


class SessionInfoForm(forms.ModelForm):
    class Meta:
        model = SessionInfo
        fields = '__all__'


class GroupMappingForm(forms.ModelForm):
    Students = forms.ModelMultipleChoiceField(queryset=MemberInfo.objects.filter(Is_Student=True),
                                              widget=FilteredSelectMultiple("Students", is_stacked=False))

    class Media:
        css = {'all': ('/static/admin/css/widgets.css',), }
        js = ('/admin/jsi18n/',)

    class Meta:
        model = GroupMapping
        fields = '__all__'


class InningGroupForm(forms.ModelForm):
    Teacher_Code = forms.ModelMultipleChoiceField(queryset=MemberInfo.objects.filter(Is_Teacher=True),
                                                  widget=FilteredSelectMultiple("Students", is_stacked=False))

    class Media:
        css = {'all': ('/static/admin/css/widgets.css',), }
        js = ('/admin/jsi18n/',)

    class Meta:
        model = InningGroup
        fields = '__all__'


class InningInfoForm(forms.ModelForm):
    Course_Group = forms.ModelMultipleChoiceField(queryset=InningGroup.objects.all(),
                                                  widget=FilteredSelectMultiple("Groups", is_stacked=False))

    class Media:
        css = {'all': ('/static/admin/css/widgets.css',), }
        js = ('/admin/jsi18n/',)

    class Meta:
        model = InningInfo
        fields = '__all__'

# AssignmentInfoForms
class AssignmentInfoForm(forms.ModelForm):
    class Meta:
        model = AssignmentInfo
        fields = '__all__'


class QuestionInfoForm(forms.ModelForm):
    class Meta:
        model = QuestionInfo
        fields = '__all__'


class AssignAssignmentInfoForm(forms.ModelForm):
    class Meta:
        model = AssignAssignmentInfo
        fields = '__all__'


class AssignAnswerInfoForm(forms.ModelForm):
    class Meta:
        model = AssignAnswerInfo
        fields = '__all__'


class MessageInfoForm(forms.ModelForm):
    class Meta:
        model = MessageInfo
        fields = '__all__'


class ChangeOthersPasswordForm(forms.Form):
    attrs = {
        "type": "password"
    }
    password = forms.CharField(widget=forms.TextInput(attrs=attrs))





