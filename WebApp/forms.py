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
from django_summernote.widgets import SummernoteWidget

from .models import CenterInfo, MemberInfo, SessionInfo, InningInfo, InningGroup, GroupMapping, MessageInfo, \
    CourseInfo, ChapterInfo, AssignmentInfo, AssignmentQuestionInfo, AssignAssignmentInfo, AssignAnswerInfo, \
    InningManager, Attendance, DepartmentInfo


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
    Use_Flag = forms.BooleanField(initial=True, required=False, label='Status')
    Member_BirthDate = forms.DateField(widget=SelectDateWidget(
        years=range(1985, datetime.date.today().year + 10)), required=False)
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
                                   'Member_Department', wrapper_class='col-md-6 col-sm-6 col-xs-12'),
                               Field(
                                   'Member_Position', wrapper_class='col-md-6 col-sm-6 col-xs-12'),
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
        fields = 'Member_ID', 'first_name', 'last_name', 'Member_Gender', 'username', 'password', 'email', \
                 'Member_Permanent_Address', 'Member_Temporary_Address', 'Member_BirthDate', 'Member_Phone', \
                 'Member_Avatar', 'Member_Memo', 'Is_Teacher', 'Is_Student', 'Use_Flag', 'Member_Department', \
                 'Member_Position'

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        super().__init__(*args, **kwargs)
        self.fields['Member_Department'].queryset = DepartmentInfo.objects.filter(Use_Flag=True,
                                                                                  Center_Code=self.request.user.Center_Code)




class MemberUpdateForm(forms.ModelForm):
    helper = FormHelper()
    Member_BirthDate = forms.DateField(widget=SelectDateWidget(
        years=range(1985, datetime.date.today().year + 10)), required=False)
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
                               Field(
                                   'Member_Department', wrapper_class='col-md-6 col-sm-6 col-xs-12'),
                               Field(
                                   'Member_Position', wrapper_class='col-md-6 col-sm-6 col-xs-12'),
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
        fields = 'Member_ID', 'first_name', 'last_name', 'Member_Gender', 'username', 'email', \
                 'Member_Permanent_Address', 'Member_Temporary_Address', 'Member_BirthDate', 'Member_Phone', \
                 'Member_Avatar', 'Member_Memo', 'Is_Teacher', 'Is_Student', 'Member_Department', \
                 'Member_Position'

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        super().__init__(*args, **kwargs)
        self.fields['Member_Department'].queryset = DepartmentInfo.objects.filter(Use_Flag=True,
                                                                                  Center_Code=self.request.user.Center_Code)


class CourseInfoForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        super().__init__(*args, **kwargs)
        self.fields['Course_Provider'].initial = self.request.user.Center_Code
        if '/edit' in self.request.path:
            del self.fields['Register_Agent']

    class Meta:
        model = CourseInfo
        fields = '__all__'

    def clean(self):
        cleaned_data = super().clean()
        name = cleaned_data.get('Course_Name')
        course = CourseInfo.objects.filter(Course_Name=name, Center_Code=self.request.user.Center_Code)
        if course.exists():
            if self.instance.id:
                if course.filter(pk=self.instance.id, Center_Code=self.request.user.Center_Code).exists():
                    if course.get(pk=self.instance.id).Course_Name == name:
                        return cleaned_data
            raise forms.ValidationError('Course Name already Exists')



class ChapterInfoForm(forms.ModelForm):
    mustreadtime = forms.CharField(label="Running Time (in minutes)", widget=forms.NumberInput(attrs={'min': '0'}))
    class Meta:
        model = ChapterInfo
        fields = ['Chapter_No', 'Chapter_Name', 'Summary', 'Page_Num', 'mustreadtime', 'Use_Flag', 'Register_Agent',
                  'is_commentable', 'Course_Code']

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        super().__init__(*args, **kwargs)
        if '/edit' in self.request.path:
            del self.fields['Register_Agent']

    def clean(self):
        pass1, pass2 = False, False
        cleaned_data = super().clean()
        num = cleaned_data.get('Chapter_No')
        name = cleaned_data.get('Chapter_Name')
        course = cleaned_data.get('Course_Code')
        chapternum = ChapterInfo.objects.filter(Course_Code=course, Chapter_No=num)
        chaptername = ChapterInfo.objects.filter(Course_Code=course, Chapter_Name__iexact=name)
        if chapternum.exists():
            if self.instance.id:
                if chapternum.filter(pk=self.instance.id, Course_Code=course).exists():
                    if chapternum.get(pk=self.instance.id).Chapter_No == num:
                        pass1 = True
            if not pass1:
                raise forms.ValidationError('Chapter Number or Chapter Name already Exists')
        if chaptername.exists():
            if self.instance.id:
                if chaptername.filter(pk=self.instance.id, Course_Code=course).exists():
                    if chaptername.get(pk=self.instance.id).Chapter_Name == name:
                        pass2 = True
            if not pass2:
                raise forms.ValidationError('Chapter Number or Chapter Name already Exists')

        if pass1 and pass2:
            return cleaned_data



class SessionInfoForm(forms.ModelForm):
    class Meta:
        model = SessionInfo
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        super(SessionInfoForm, self).__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        name = cleaned_data.get('Session_Name')
        session = SessionInfo.objects.filter(Session_Name=name, Center_Code=self.request.user.Center_Code)
        if session.exists():
            if self.instance.id:
                if session.filter(pk=self.instance.id, Center_Code=self.request.user.Center_Code).exists():
                    if session.get(pk=self.instance.id).Session_Name == name:
                        return cleaned_data
            raise forms.ValidationError('Session Name already Exists')



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
        if '/update' in self.request.path:
            del self.fields['Register_Agent']

    def clean(self):
        cleaned_data = super().clean()
        name = cleaned_data.get('GroupMapping_Name')
        groupmapping = GroupMapping.objects.filter(GroupMapping_Name=name, Center_Code=self.request.user.Center_Code)
        if groupmapping.exists():
            if self.instance.id:
                if groupmapping.filter(pk=self.instance.id, Center_Code=self.request.user.Center_Code).exists():
                    if groupmapping.get(pk=self.instance.id).GroupMapping_Name == name:
                        return cleaned_data
            raise forms.ValidationError('Group Name already Exists')


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
                                                                        Use_Flag=True).order_by('Course_Name')

        self.fields['InningGroup_Name'].label = "Course Allocation Name"
        self.fields['Course_Code'].label = "Course Code"
        if '/update' in self.request.path:
            del self.fields['Register_Agent']

    def clean(self):
        cleaned_data = super().clean()
        name = cleaned_data.get('InningGroup_Name')
        inninggroupname = InningGroup.objects.filter(InningGroup_Name=name, Center_Code=self.request.user.Center_Code)
        if inninggroupname.exists():
            if self.instance.id:
                if inninggroupname.filter(pk=self.instance.id, Center_Code=self.request.user.Center_Code).exists():
                    if inninggroupname.get(pk=self.instance.id).InningGroup_Name == name:
                        return cleaned_data
            raise forms.ValidationError('Course Allocation Name already Exists')





class CoursesMultipleChoiceField(forms.ModelMultipleChoiceField):
    """
    Custom multiple select Feild with full name
    """

    def label_from_instance(self, obj):
        return "%s (%s)" % (obj.InningGroup_Name, obj.Teacher_Code.count())



class InningInfoForm(forms.ModelForm):
    Course_Group = CoursesMultipleChoiceField(queryset=None, required=True,
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
        if '/update' in self.request.path:
            del self.fields['Register_Agent']

        # rel = ManyToOneRel(self.instance.Course_Group.model, 'id',field_name="Course Group")
        # self.fields['Course_Group'].widget = RelatedFieldWidgetWrapper(self.fields['Course_Group'].widget, rel, self.admin_site)


# AssignmentInfoForms
class AssignmentInfoForm(forms.ModelForm):
    # Assignment_Start = forms.CharField(
    #     required=True,
    # )
    # Assignment_Deadline = forms.CharField(
    #     required=True,
    # )

    class Meta:
        model = AssignmentInfo
        fields = ['Assignment_Topic', 'Use_Flag', 'Course_Code', 'Chapter_Code', 'Register_Agent', ]



class QuestionInfoForm(forms.ModelForm):
    Question_Description = forms.CharField(widget=SummernoteWidget(attrs=
                                                                   {'summernote':
                                                                        {'width': '100%', 'height': '480px',
                                                                         'toolbar': [["style", ["style"]],
                                                                                     ["font",
                                                                                      ["bold", "italic", "underline"]],
                                                                                     ["para", ["ul", "ol"]],
                                                                                     ["table", ["table"]],
                                                                                     ["insert", ["link", "picture"]],
                                                                                     ]}
                                                                    }), required=False)

    class Meta:
        model = AssignmentQuestionInfo
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(QuestionInfoForm, self).__init__(*args, **kwargs)
        self.fields['Question_Media_File'].label = "Question_Media_File (Max Size: 2 MB)"


class AssignAssignmentInfoForm(forms.ModelForm):
    class Meta:
        model = AssignAssignmentInfo
        fields = '__all__'

class AssignAnswerInfoForm(forms.ModelForm):
    Assignment_Answer = forms.CharField(widget=SummernoteWidget(attrs=
                                                                   {'summernote':
                                                                        {'width': '100%', 'height': '200px',
                                                                         'toolbar': [["style", ["style"]],
                                                                                     ["font",
                                                                                      ["bold", "italic", "underline"]],
                                                                                     ["para", ["ul", "ol"]],
                                                                                     ["table", ["table"]],
                                                                                     ["insert", ["link", "picture"]],
                                                                                     ]}
                                                                    }), required=False)
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


# Department Infos
class DepartmentInfoForm(forms.ModelForm):
    class Meta:
        model = DepartmentInfo
        fields = ['Department_Name', 'Center_Code',
                  'Register_Agent', 'Use_Flag']
        widgets = {
            'Center_Code': forms.HiddenInput(),
            'Register_Agent': forms.HiddenInput(),
            'Use_Flag': forms.HiddenInput(),
        }

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        super().__init__(*args, **kwargs)
        self.fields['Register_Agent'].initial = self.request.user.username
        self.fields['Use_Flag'].initial = True
        self.fields['Center_Code'].initial = self.request.user.Center_Code
        if '/edit' in self.request.path:
            del self.fields['Register_Agent']

    def clean(self):
        cleaned_data = super().clean()
        name = cleaned_data.get('Department_Name')
        department = DepartmentInfo.objects.filter(Department_Name=name, Center_Code=self.request.user.Center_Code)
        if department.exists():
            if self.instance.id:
                if department.filter(pk=self.instance.id, Center_Code=self.request.user.Center_Code).exists():
                    if department.get(pk=self.instance.id).Department_Name == name:
                        return cleaned_data
            raise forms.ValidationError('Department Name already Exists')


class DepartmentInfoUpdateForm(forms.ModelForm):
    class Meta:
        model = DepartmentInfo
        fields = ['Department_Name', 'Center_Code',
                  'Register_Agent', 'Use_Flag']
        widgets = {
            'Center_Code': forms.HiddenInput(),
            'Register_Agent': forms.HiddenInput(),

        }

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        super().__init__(*args, **kwargs)
        self.fields['Register_Agent'].initial = self.request.user.username
        self.fields['Center_Code'].initial = self.request.user.Center_Code
        self.fields['Use_Flag'].label = 'Active'
