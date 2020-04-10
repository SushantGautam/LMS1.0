# from django.db.models.fields.reverse_related import ManyToOneRel
# from django.contrib.admin.widgets import RelatedFieldWidgetWrapper
import datetime

from crispy_forms.bootstrap import Accordion, AccordionGroup, FormActions
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Field, HTML, Submit
from django import forms
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.contrib.auth.forms import UserCreationForm
from django.forms import SelectDateWidget

from .models import CenterInfo, MemberInfo, SessionInfo, InningInfo, InningGroup, GroupMapping, MessageInfo, \
    CourseInfo, ChapterInfo, AssignmentInfo, AssignmentQuestionInfo, AssignAssignmentInfo, AssignAnswerInfo, \
    InningManager, Attendance


class UserRegisterForm(UserCreationForm):
    # Member_Role = forms.MultipleChoiceField(choices=USER_ROLES, widget=forms.CheckboxSelectMultiple())

    class Meta(UserCreationForm.Meta):
        Member_BirthDate = forms.DateField(widget=SelectDateWidget(
            years=range(1955, datetime.date.today().year - 10)))
        model = MemberInfo
        fields = ('username', 'email', 'Member_Gender',
                  'Center_Code', 'Is_Student', 'Is_Teacher', 'Use_Flag')


class UserUpdateForm(forms.ModelForm):
    # role = forms.MultipleChoiceField(choices=USER_ROLES, )
    Member_BirthDate = forms.DateField(widget=SelectDateWidget(
        years=range(1985, datetime.date.today().year + 10)))

    class Meta:
        model = MemberInfo
        fields = (
            'email', 'Member_Permanent_Address',
            'Member_Temporary_Address', 'Member_BirthDate', 'Member_Phone', 'Member_Avatar',)


class UserUpdateFormForAdmin(forms.ModelForm):
    class Meta:
        model = MemberInfo
        fields = '__all__'
        widgets = {
            'role': forms.CheckboxSelectMultiple,
        }


class CenterInfoForm(forms.ModelForm):
    class Meta:
        model = CenterInfo
        fields = ['Center_Name', 'Center_Address',
                  'Use_Flag', 'Register_Agent']


class MemberInfoForm(forms.ModelForm):
    Use_Flag = forms.BooleanField(initial=True, required=False)
    Member_BirthDate = forms.DateField(widget=SelectDateWidget(
        years=range(1985, datetime.date.today().year + 10)))
    password = forms.CharField(initial='00000')
    helper = FormHelper()
    helper.layout = Layout(

        Accordion(
            AccordionGroup('Basic Information',

                           Div(
                               Field(
                                   'Member_ID', wrapper_class='col-md-6 col-sm-6 col-xs-12'),
                               Field(
                                   'Member_Gender', wrapper_class='col-md-6 col-sm-6 col-xs-12'),
                               css_class='row'),

                           Div(
                               Field(
                                   'first_name', wrapper_class='col-md-6 col-sm-6 col-xs-12'),
                               Field(
                                   'last_name', wrapper_class='col-md-6 col-sm-6 col-xs-12'),
                               css_class='row'),

                           Div(
                               Field(
                                   'username', wrapper_class='col-md-6 col-sm-6 col-xs-12'),
                               Field(
                                   'password', wrapper_class='col-md-6 col-sm-6 col-xs-12'),
                               css_class='row'),

                           Div(
                               Field(
                                   'email', wrapper_class='col-md-6 col-sm-6 col-xs-12'),
                               HTML('''<div class='col-md-6'></div>'''),
                               css_class='row'),

                           Div(
                               Field(
                                   'Is_Teacher', wrapper_class='col-md-6 col-sm-6 col-xs-12'),
                               Field(
                                   'Is_Student', wrapper_class='col-md-6 col-sm-6 col-xs-12'),
                               css_class='row'),
                           css_class='collapse'),

            AccordionGroup('Additional Information',

                           Div(
                               Field('Member_Permanent_Address',
                                     wrapper_class='col-md-6 col-sm-6 col-xs-12'),
                               Field('Member_Temporary_Address',
                                     wrapper_class='col-md-6 col-sm-6 col-xs-12'),
                               css_class='row'),

                           Div(
                               Field('Member_BirthDate',
                                     wrapper_class='col-md-6 col-sm-6 col-xs-12'),
                               Field(
                                   'Member_Phone', wrapper_class='col-md-6 col-sm-6 col-xs-12'),
                               css_class='row'),

                           Div(
                               Field(
                                   'Member_Avatar', wrapper_class='col-md-6 col-sm-6 col-xs-12'),
                               Field(
                                   'Member_Memo', wrapper_class='col-md-6 col-sm-6 col-xs-12'),
                               css_class='row'),
                           )
        ),
        FormActions(
            Submit('submit', 'Create Member', css_class='btn btn-success'),
            HTML(
                ''' <button class='btn btn-primary' id="saveandnew" type="submit" formtarget="_blank"> Save and New </button> ''')
            # Button('cancel', 'Cancel')
        )
    )

    class Meta:
        model = MemberInfo
        Member_BirthDate = forms.DateField(widget=SelectDateWidget(
            years=range(1985, datetime.date.today().year + 10)))
        fields = 'Member_ID', 'first_name', 'last_name', 'Member_Gender', 'username', 'password', 'email', 'Member_Permanent_Address', 'Member_Temporary_Address', 'Member_BirthDate', 'Member_Phone', 'Member_Avatar', 'Member_Memo', 'Is_Teacher', 'Is_Student', 'Use_Flag'


class MemberUpdateForm(forms.ModelForm):
    helper = FormHelper()
    Member_BirthDate = forms.DateField(widget=SelectDateWidget(
        years=range(1985, datetime.date.today().year + 10)))
    helper.layout = Layout(

        Accordion(
            AccordionGroup('Basic Information',

                           Div(
                               Field(
                                   'Member_ID', wrapper_class='col-md-6 col-sm-6 col-xs-12'),
                               Field(
                                   'Member_Gender', wrapper_class='col-md-6 col-sm-6 col-xs-12'),
                               css_class='row'),

                           Div(
                               Field(
                                   'first_name', wrapper_class='col-md-6 col-sm-6 col-xs-12'),
                               Field(
                                   'last_name', wrapper_class='col-md-6 col-sm-6 col-xs-12'),
                               css_class='row'),

                           Div(
                               Field(
                                   'username', wrapper_class='col-md-6 col-sm-6 col-xs-12'),
                               Field(
                                   'email', wrapper_class='col-md-6 col-sm-6 col-xs-12'),
                               css_class='row'),

                           Div(
                               Field('Is_Teacher', 'Is_Student',
                                     wrapper_class='col-md-3 col-sm-6 col-xs-12'),
                           ),
                           css_class='collapse'),

            AccordionGroup('Additional Information',

                           Div(
                               Field('Member_Permanent_Address',
                                     wrapper_class='col-md-6 col-sm-6 col-xs-12'),
                               Field('Member_Temporary_Address',
                                     wrapper_class='col-md-6 col-sm-6 col-xs-12'),
                               css_class='row'),

                           Div(
                               Field('Member_BirthDate',
                                     wrapper_class='col-md-6 col-sm-6 col-xs-12'),
                               Field(
                                   'Member_Phone', wrapper_class='col-md-6 col-sm-6 col-xs-12'),
                               Field(
                                   'Member_Memo', wrapper_class='col-md-6 col-sm-6 col-xs-12'),
                               css_class='row'),

                           Div(
                               Field(
                                   'Member_Avatar', wrapper_class='col-md-6 col-sm-6 col-xs-12'),
                               css_class='row'),
                           )
        ),
        FormActions(
            Submit('submit', 'Save changes'),
            # Button('cancel', 'Cancel')
        )
    )

    # helper.add_input(Submit('submit', 'Submit', css_class='btn-primary'))

    class Meta:
        model = MemberInfo
        fields = 'Member_ID', 'first_name', 'last_name', 'Member_Gender', 'username', 'email', 'Member_Permanent_Address', 'Member_Temporary_Address', 'Member_BirthDate', 'Member_Phone', 'Member_Avatar', 'Member_Memo', 'Is_Teacher', 'Is_Student'


class CourseInfoForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        super().__init__(*args, **kwargs)
        self.fields['Course_Provider'].initial = self.request.user.Center_Code

    class Meta:
        model = CourseInfo
        fields = '__all__'


class ChapterInfoForm(forms.ModelForm):
    mustreadtime = forms.CharField(label="Running Time (in minutes)", widget=forms.NumberInput(attrs={'min': '0'}))
    Start_Date = forms.CharField(
        required=False,
    )
    End_Date = forms.CharField(
        required=False,
    )

    class Meta:
        model = ChapterInfo
        fields = '__all__'


class SessionInfoForm(forms.ModelForm):
    class Meta:
        model = SessionInfo
        fields = '__all__'


class GroupMappingForm(forms.ModelForm):
    Students = forms.ModelMultipleChoiceField(queryset=None, required=True,
                                              widget=FilteredSelectMultiple("Students", is_stacked=False))

    class Media:
        css = {'all': ('/static/admin/css/widgets.css',), }
        js = ('/static/build/js/jsi18n.js',)

    class Meta:
        model = GroupMapping
        fields = '__all__'

    # To filter out only active students of that center
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        super(GroupMappingForm, self).__init__(*args, **kwargs)
        self.fields['Students'].queryset = MemberInfo.objects.filter(Is_Student=True, Use_Flag=True,
                                                                     Center_Code=self.request.user.Center_Code)


class InningGroupForm(forms.ModelForm):
    Teacher_Code = forms.ModelMultipleChoiceField(queryset=None, required=True,
                                                  widget=FilteredSelectMultiple("Teachers", is_stacked=False))

    class Media:
        css = {'all': ('/static/admin/css/widgets.css',), }
        js = ('/static/build/js/jsi18n.js',)

    class Meta:
        model = InningGroup
        fields = '__all__'

    # To filter out only active teachers of that center
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        super(InningGroupForm, self).__init__(*args, **kwargs)
        self.fields['Teacher_Code'].queryset = MemberInfo.objects.filter(Is_Teacher=True, Use_Flag=True,
                                                                         Center_Code=self.request.user.Center_Code)
        self.fields['Course_Code'].queryset = CourseInfo.objects.filter(Center_Code=self.request.user.Center_Code,
                                                                        Use_Flag=True)


class InningInfoForm(forms.ModelForm):
    Course_Group = forms.ModelMultipleChoiceField(queryset=None, required=True,
                                                  widget=FilteredSelectMultiple("Courses", is_stacked=False))

    class Media:
        css = {'all': ('/static/admin/css/widgets.css',), }
        js = ('/static/build/js/jsi18n.js',)

    class Meta:
        model = InningInfo
        fields = '__all__'

    # To filter out only active course group of that center
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        super(InningInfoForm, self).__init__(*args, **kwargs)
        self.fields['Course_Group'].queryset = InningGroup.objects.filter(Use_Flag=True,
                                                                          Center_Code=self.request.user.Center_Code)
        self.fields['Inning_Name'].queryset = SessionInfo.objects.filter(Center_Code=self.request.user.Center_Code,
                                                                         Use_Flag=True)
        self.fields['Groups'].queryset = GroupMapping.objects.filter(Center_Code=self.request.user.Center_Code,
                                                                     Use_Flag=True)

        # rel = ManyToOneRel(self.instance.Course_Group.model, 'id',field_name="Course Group")
        # self.fields['Course_Group'].widget = RelatedFieldWidgetWrapper(self.fields['Course_Group'].widget, rel, self.admin_site)


# AssignmentInfoForms
class AssignmentInfoForm(forms.ModelForm):
    class Meta:
        model = AssignmentInfo
        fields = '__all__'


class QuestionInfoForm(forms.ModelForm):
    class Meta:
        model = AssignmentQuestionInfo
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


class AchievementPage_All_form(forms.Form):
    studentfilter = forms.CharField()
    Inningsfilter = forms.ModelChoiceField(queryset=InningInfo.objects.none())
    GroupMappingFilter = forms.ModelChoiceField(
        queryset=GroupMapping.objects.none())

    def __init__(self, *args, **kwargs):
        super(AchievementPage_All_form, self).__init__(*args, **kwargs)
        self.fields['Inningsfilter'].queryset = kwargs['initial']['Inningsfilter']
        self.fields['GroupMappingFilter'].queryset = kwargs['initial']['GroupMappingFilter']

        # (choice.pk, choice) for choice in studentfilter]


class InningManagerForm(forms.ModelForm):
    memberinfoobj = forms.ModelMultipleChoiceField(queryset=MemberInfo.objects.all(), required=False,
                                                   widget=FilteredSelectMultiple("Members", is_stacked=False),
                                                   label="Please select Session Admin(s)")

    class Meta:
        model = InningManager
        fields = '__all__'
        widgets = {
            'sessioninfoobj': forms.HiddenInput(),
        }

    class Media:
        css = {'all': ('/static/admin/css/widgets.css',), }
        js = ('/static/build/js/jsi18n.js',)

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        super().__init__(*args, **kwargs)
        self.fields['memberinfoobj'].queryset = MemberInfo.objects.filter(Use_Flag=True,
                                                                          Center_Code=self.request.user.Center_Code,
                                                                          Is_Teacher=True)


class AttendanceForm(forms.ModelForm):
    attendance_date = forms.DateTimeField(
        input_formats=['%Y-%m-%dT%H:%M'],
        widget=forms.DateTimeInput(
            attrs={
                'type': 'datetime-local',
                'class': 'form-control'},
            format='%Y-%m-%d')
    )

    class Meta:
        model = Attendance
        fields = ['present', 'member_code', 'course', 'attendance_date']


from django.forms.models import modelformset_factory

AttendanceFormSetForm = modelformset_factory(Attendance,
                                             fields=['present', 'member_code', 'course', 'attendance_date', 'id']
                                             )


class AttendanceFormSetFormT(forms.ModelForm):
    # attendance_date = forms.DateTimeField(
    #     input_formats=['%Y-%m-%dT%H:%M'],
    #     widget=forms.DateTimeInput(
    #         attrs={
    #             'type': 'datetime-local',
    #             'class': 'form-control'},
    #         format='%Y-%m-%d')
    # )
    # present = forms.BooleanField(label='')

    class Meta:
        model = Attendance
        fields = ['present', 'member_code', 'course', 'attendance_date']
        widgets = {'member_code': forms.HiddenInput(),
                   'course': forms.HiddenInput(),
                   'attendance_date': forms.HiddenInput(), }
        labels = {
            "present": "", }
