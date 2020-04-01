import os
from datetime import datetime
from time import timezone

from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError
from django.core.files.storage import FileSystemStorage
from django.db import models as models
from django.db.models import ForeignKey, CharField, IntegerField, DateTimeField, TextField, BooleanField, ImageField, \
    FileField
from django.db.models.signals import post_delete
from django.dispatch import receiver
from django.urls import reverse
from django.utils.translation import gettext as _

# from quiz.models import Quiz

fs = FileSystemStorage(location='LMS')

USER_ROLES = (
    ('CenterAdmin', 'CenterAdmin'),
    ('Teacher', 'Teacher'),
    ('Student', 'Student'),
    ('Parent', 'Parent'),
)


class CenterInfo(models.Model):
    Center_Name = CharField(max_length=500, blank=True, null=True)
    Center_Address = CharField(max_length=500, blank=True, null=True)
    Use_Flag = BooleanField(default=True)
    Register_Agent = CharField(max_length=500, blank=True, null=True)
    Register_DateTime = DateTimeField(auto_now_add=True)
    Updated_DateTime = DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-pk',)

    def __str__(self):
        return self.Center_Name

    def __unicode__(self):
        return u'%s' % self.pk

    def get_absolute_url(self):
        return reverse('centerinfo_detail', args=(self.pk,))

    def get_update_url(self):
        return reverse('centerinfo_update', args=(self.pk,))

    def get_delete_url(self):
        return reverse('centerinfo_delete', args=(self.pk,))


class MemberInfo(AbstractUser):
    Gender_Choices = (
        ('M', 'Male'),
        ('F', 'Female'),
    )
    username_validator = UnicodeUsernameValidator()

    username = models.CharField(
        _('        Username for Login'),
        max_length=150,
        unique=True,
        help_text=_('Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only. Unique in the system.'),
        validators=[username_validator],
        error_messages={
            'unique': _("A user with that username already exists."),
        },
    )
    first_name = models.CharField(_('first name'), max_length=50, blank=True)
    last_name = models.CharField(_('last name'), max_length=50, blank=True)
    email = models.EmailField(_('email address'), blank=True)
    is_staff = models.BooleanField(
        _('staff status'),
        default=True,  # to make admin widgets accessible
        help_text=_('Designates whether the user can log into this admin site.'),
    )
    is_superuser = models.BooleanField(
        _('is_superuser status'),
        default=False,
        help_text=_('Designates whether the user is superuser'),
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )

    Member_ID = models.CharField(max_length=150, blank=True, null=True, verbose_name='Registration ID',

                                 help_text=_('ID assigned by university/Roll No'))
    password = models.CharField(_('password'), max_length=264)
    Member_Permanent_Address = models.CharField(max_length=500, blank=True, null=True)
    Member_Temporary_Address = models.CharField(max_length=500, blank=True, null=True)
    Member_BirthDate = models.DateTimeField(blank=True, null=True)
    Member_Phone = models.CharField(max_length=150, blank=True, null=True)
    Use_Flag = BooleanField(default=True)
    Register_DateTime = DateTimeField(auto_now_add=True)
    Register_Agent = CharField(max_length=128, blank=True, null=True)
    Updated_DateTime = DateTimeField(auto_now=True)
    Member_Memo = models.TextField(blank=True, null=True)
    Member_Avatar = models.ImageField(upload_to="Member_images/", blank=True, null=True)
    Is_Teacher = models.BooleanField(default=False)
    Is_Student = models.BooleanField(default=True)
    Is_CenterAdmin = models.BooleanField(default=False)
    Is_Parent = models.BooleanField(default=False)
    Member_Gender = models.CharField(max_length=1, choices=Gender_Choices, default='F')

    # Relationship Fields
    Center_Code = ForeignKey(
        'CenterInfo',
        related_name="memberinfos", on_delete=models.DO_NOTHING, null=True
    )

    def get_student_courses(self):
        innings = InningInfo.objects.filter(Groups__in=GroupMapping.objects.filter(Students__pk=self.pk),
                                            End_Date__gt=datetime.now())
        courses = InningGroup.objects.filter(inninginfo__in=innings).values_list('Course_Code__pk')
        return courses

    def get_teacher_courses(self):
        courses = []
        session_list = []
        ig = InningGroup.objects.filter(Teacher_Code__pk=self.pk)
        for i in ig:
            inning_info = InningInfo.objects.filter(Course_Group__Teacher_Code__pk=self.pk,
                                                    Course_Group__pk=i.pk, Use_Flag=True,
                                                    End_Date__gt=datetime.now()).distinct()
            if inning_info.exists():
                courses.append(i.Course_Code)
                session_list.append(inning_info)
        return {'courses': courses, 'session': session_list}

    @property
    def get_user_type(self):
        if self.Is_CenterAdmin and self.Is_Teacher and self.Is_Student:
            return "Center Admin, Teacher, Student"
        elif self.Is_CenterAdmin and self.Is_Teacher:
            return "Center Admin, Teacher"
        elif self.Is_CenterAdmin and self.Is_Student:
            return "Center Admin, Student"
        elif self.Is_Teacher and self.Is_Student:
            return "Teacher, Student"
        elif self.Is_CenterAdmin:
            return "Center Admin"
        elif self.Is_Teacher:
            return "Teacher"
        elif self.Is_Student:
            return "Student"

    @property
    def Avatar(self):
        if self.Member_Avatar:
            default_avatar = self.Member_Avatar.url
        else:
            if self.Member_Gender == 'F':
                default_avatar = '/static/images/profile/female.png'
            elif self.Member_Gender == 'M':
                default_avatar = '/static/images/profile/male.jpg'
            else:
                default_avatar = '/static/images/profile/profile.png'
        return default_avatar

    class Meta:
        ordering = ('-pk',)

    def __unicode__(self):
        return u'%s' % self.pk

    def get_absolute_url(self):
        return reverse('memberinfo_detail', args=(self.pk,))

    def get_update_url(self):
        return reverse('memberinfo_update', args=(self.pk,))

    def __str__(self):
        return self.first_name + " " + self.last_name + " (" + self.username + ")"
        # if self.first_name and self.last_name:
        #     return self.first_name + " " + self.last_name + " (" + self.username + ")"
        # else:
        #     return "-- (" + self.username + ")"

    def getFullName(self):
        if self.first_name or self.last_name:
            return self.first_name + " " + self.last_name
        else:
            return "-- (" + self.username + ")"

    # def create_user(self, username, email=None, password=None, **extra_fields):
    #     extra_fields.setdefault('is_staff', True)
    #     extra_fields.setdefault('is_superuser', True)
    #     return self._create_user(username, email, password, **extra_fields)


class CourseInfo(models.Model):
    Course_Name = CharField(max_length=240)
    Course_Description = TextField(blank=True, null=True)
    Course_Cover_File = ImageField(upload_to="Course_images/", blank=True, null=True)
    Course_Level = IntegerField(default=1, blank=True, null=True)
    Course_Info = TextField(blank=True, null=True)

    Use_Flag = BooleanField(default=True, verbose_name="Tick this flag if you want to prevent user from login.")
    Register_DateTime = DateTimeField(auto_now_add=True)
    Updated_DateTime = DateTimeField(auto_now=True)
    Register_Agent = CharField(max_length=500, blank=True, null=True)

    Course_Provider = CharField(max_length=250, blank=True, null=True)

    # Relationship Fields
    Center_Code = ForeignKey(
        'CenterInfo',
        related_name="courseinfos", on_delete=models.DO_NOTHING)

    class Meta:
        ordering = ('-pk',)

    def __unicode__(self):
        return u'%s' % self.pk

    def student_get_absolute_url(self):
        return reverse('student_courseinfo_detail', args=(self.pk,))

    def teacher_get_absolute_url(self):
        return reverse('teacher_courseinfo_detail', args=(self.pk,))

    def get_absolute_url(self):
        return reverse('courseinfo_detail', args=(self.pk,))

    def get_update_url(self):
        return reverse('courseinfo_update', args=(self.pk,))

    def get_teachers_of_this_course(self):
        teachers_of_this_course_id = InningGroup.objects.filter(Course_Code=self.pk).values('Teacher_Code')
        teachers_of_this_course = MemberInfo.objects.filter(pk__in=teachers_of_this_course_id)
        return teachers_of_this_course

    # def get_exam_quiz(self):
    #     return Quiz.objects.get(exam_paper=True, course_code=self.id)

    def __str__(self):
        return self.Course_Name


class ChapterInfo(models.Model):
    Chapter_No = IntegerField()
    Chapter_Name = CharField(max_length=200)
    Summary = TextField(blank=True, null=True)
    Page_Num = IntegerField(blank=True, null=True)
    mustreadtime = IntegerField(blank=True, null=True)
    Use_Flag = BooleanField(default=True)
    Register_DateTime = DateTimeField(auto_now_add=True)
    Updated_DateTime = DateTimeField(auto_now=True)
    Start_Date = DateTimeField(null=True, blank=True)
    End_Date = DateTimeField(null=True, blank=True)
    Register_Agent = CharField(max_length=500, blank=True, null=True)

    # Relationship Fields
    Course_Code = ForeignKey(
        'CourseInfo',
        related_name="chapterinfos", on_delete=models.CASCADE
    )

    class Meta:
        ordering = ('pk',)

    def __unicode__(self):
        return u'%s' % self.pk

    def student_get_absolute_url(self):
        return reverse('student_chapterinfo_detail', args=(self.Course_Code.id, self.pk,))

    def teacher_get_absolute_url(self):
        return reverse('teacher_chapterinfo_detail', args=(self.Course_Code.id, self.pk,))

    def get_absolute_url(self):
        return reverse('chapterinfo_detail', args=(self.Course_Code.id, self.pk,))

    def get_update_url(self):
        return reverse('chapterinfo_update', args=(self.Course_Code.id, self.pk,))

    def getmustreadtimeinformat(self):
        return str(int(self.mustreadtime / 3600)) + ':' + str(int(self.mustreadtime % 3600 / 60)) + ':' + str(
            int(self.mustreadtime % 60)) if self.mustreadtime is not None else None

    def __str__(self):
        return self.Chapter_Name

    def clean(self):
        super().clean()
        if (self.Start_Date > self.End_Date):
            raise ValidationError('End Date must be greater than start date')

class ChapterContentsInfo(models.Model):
    Use_Flag = BooleanField(default=True)
    Register_DateTime = DateTimeField(auto_now_add=True)
    Updated_DateTime = DateTimeField(auto_now=True)
    Register_Agent = CharField(max_length=500, blank=True, null=True)
    Content_Description = TextField(blank=True, null=True)

    # Relationship Fields
    Chapter_Code = ForeignKey(
        'ChapterInfo',
        related_name="chaptercontentsinfos", on_delete=models.DO_NOTHING
    )

    class Meta:
        ordering = ('-pk',)

    def __unicode__(self):
        return u'%s' % self.pk

    def get_absolute_url(self):
        return reverse('chaptercontentsinfo_detail', args=(self.pk,))

    def get_update_url(self):
        return reverse('chaptercontentsinfo_update', args=(self.pk,))


# ================AssignmentModels================#
from datetime import timedelta
from django.utils import timezone


def in_three_days():
    return timezone.now() + timedelta(days=3)


class AssignmentInfo(models.Model):
    Assignment_Topic = CharField(max_length=500)
    Use_Flag = BooleanField(default=True)
    Register_DateTime = DateTimeField(auto_now_add=True)
    Updated_DateTime = DateTimeField(auto_now=True)
    Assignment_Start = DateTimeField(default=timezone.now)
    Assignment_Deadline = DateTimeField(default=in_three_days)
    Course_Code = ForeignKey(
        'CourseInfo',
        related_name="assignmentinfos", on_delete=models.CASCADE
    )
    Chapter_Code = ForeignKey(
        'ChapterInfo',
        related_name="assignmentinfos", on_delete=models.CASCADE)
    Register_Agent = ForeignKey(
        'MemberInfo',
        related_name="assignmentinfos", on_delete=models.CASCADE
    )

    def __str__(self):
        return self.Assignment_Topic

    def student_get_absolute_url(self):
        return reverse('student_assignmentinfo_detail', args=(self.Course_Code.id, self.Chapter_Code.id, self.pk,))

    def teacher_get_absolute_url(self):
        return reverse('teacher_assignmentinfo_detail', args=(self.Course_Code.id, self.Chapter_Code.id, self.pk,))

    def teacher_get_update_url(self):
        return reverse('teacher_assignmentinfo_update', args=(self.Course_Code.id, self.Chapter_Code.id, self.pk,))

    def get_absolute_url(self):
        return reverse('assignmentinfo_detail', args=(self.Course_Code.id, self.Chapter_Code.id, self.pk,))

    def get_update_url(self):
        return reverse('assignmentinfo_update', args=(self.Course_Code.id, self.Chapter_Code.id, self.pk,))

    def get_student_assignment_status(self, user):
        status = False
        questions = AssignmentQuestionInfo.objects.filter(
            Assignment_Code=self.pk)
        answers = []
        AnsweredQuestion = set()
        Question = set()
        for question in questions:
            Answer = AssignAnswerInfo.objects.filter(
                Student_Code=user.pk, Question_Code=question.id)
            answers += Answer
            Question.add(question.id)
        for ans in answers:
            # print (answers.Question_Code.id)
            AnsweredQuestion.add(ans.Question_Code.id)
        unanswered = Question - AnsweredQuestion
        if not unanswered:
            status = True
        print(status)
        return status


def upload_to(instance, filename):
    return 'questions/{0}/{1}'.format(instance.id, filename)


class AssignmentQuestionInfo(models.Model):
    Question_Title = CharField(max_length=4000)
    Question_Score = IntegerField(blank=False, null=True, default=10)
    Use_Flag = BooleanField(default=True)
    Register_DateTime = DateTimeField(auto_now_add=True)
    Updated_DateTime = DateTimeField(auto_now=True)

    Question_Media_File = FileField(upload_to=upload_to, blank=True, null=True)
    Question_Description = TextField()
    Answer_Choices = (
        ('S', 'Short Answer'),
        ('F', 'File Upload'),
    )
    Answer_Type = CharField(max_length=1, choices=Answer_Choices, default='S')

    Assignment_Code = ForeignKey(
        'AssignmentInfo',
        related_name="questioninfos", on_delete=models.CASCADE
    )

    Register_Agent = ForeignKey(
        'MemberInfo',
        related_name="questioninfos", on_delete=models.CASCADE
    )

    class Meta:
        ordering = ('pk',)

    def __unicode__(self):
        return u'%s' % self.pk

    def get_absolute_url(self):
        return reverse('webapp_questioninfo_detail', args=(
            self.Assignment_Code.Course_Code.pk, self.Assignment_Code.Chapter_Code.pk, self.Assignment_Code.pk,
            self.pk))

    def get_update_url(self):
        return reverse('webapp_questioninfo_update', args=(
            self.Assignment_Code.Course_Code.pk, self.Assignment_Code.Chapter_Code.pk, self.Assignment_Code.pk,
            self.pk))

    def extension(self):
        name, extension = os.path.splitext(self.Question_Media_File.name)
        return extension


class AssignAssignmentInfo(models.Model):
    Use_Flag = BooleanField(default=True)
    Register_DateTime = DateTimeField(auto_now_add=True)
    Updated_DateTime = DateTimeField(auto_now=True)

    # Relationship Fields
    Inning_Code = ForeignKey(
        'InningInfo',
        related_name="assignassignmentinfos", on_delete=models.CASCADE
    )
    Assignment_Code = ForeignKey(
        'AssignmentInfo',
        related_name="assignassignmentinfos", on_delete=models.CASCADE
    )
    Assigned_By = ForeignKey(
        'MemberInfo',
        related_name="assignassignmentinfos", on_delete=models.CASCADE
    )

    class Meta:
        ordering = ('-pk',)

    def __unicode__(self):
        return u'%s' % self.pk

    def get_absolute_url(self):
        return reverse('assignassignmentinfo_detail', args=(self.pk,))

    def get_update_url(self):
        return reverse('assignassignmentinfo_update', args=(self.pk,))


def assignment_upload(instance, filename):
    return 'assignments/{0}/{1}'.format(instance.Question_Code.Assignment_Code.id, filename)


class AssignAnswerInfo(models.Model):
    Assignment_Score = IntegerField(blank=True, null=True)
    Use_Flag = BooleanField(default=True)
    Register_DateTime = DateTimeField(auto_now_add=True)
    Updated_DateTime = DateTimeField(auto_now=True)
    Assignment_Answer = TextField(null=True, blank=True)
    Assignment_File = FileField(upload_to=assignment_upload, null=True, blank=True)

    # Relationship Fields
    Question_Code = ForeignKey(
        'AssignmentQuestionInfo',
        related_name="assignanswerinfos", on_delete=models.CASCADE
    )
    Student_Code = ForeignKey(
        'MemberInfo',
        related_name="assignanswerinfos", on_delete=models.CASCADE
    )

    class Meta:
        ordering = ('-pk',)

    def __unicode__(self):
        return u'%s' % self.pk

    def get_absolute_url(self):
        return reverse('assignanswerinfo_detail', args=(self.pk,))

    def get_update_url(self):
        return reverse('assignanswerinfo_update', args=(self.pk,))


@receiver(post_delete, sender=AssignAnswerInfo)
def submission_delete(sender, instance, **kwargs):
    instance.Assignment_File.delete(False)


class SessionInfo(models.Model):
    Session_Name = CharField(max_length=200)
    Description = TextField(blank=True, null=True)
    Use_Flag = BooleanField(default=True)

    Center_Code = ForeignKey(
        'CenterInfo',
        related_name="sessioninfos", on_delete=models.DO_NOTHING
    )

    class Meta:
        ordering = ('-pk',)

    def __unicode__(self):
        return u'%s' % self.pk

    def get_absolute_url(self):
        return reverse('sessioninfo_detail', args=(self.pk,))

    def get_update_url(self):
        return reverse('sessioninfo_update', args=(self.pk,))

    def __str__(self):
        return self.Session_Name


class GroupMapping(models.Model):
    # Fields
    GroupMapping_Name = CharField(max_length=200)
    Use_Flag = BooleanField(default=True)
    Register_DateTime = DateTimeField(auto_now_add=True)
    Updated_DateTime = DateTimeField(auto_now=True)
    Register_Agent = CharField(max_length=500, blank=True, null=True)

    # Relationship Fields
    Students = models.ManyToManyField(
        'MemberInfo'
    )

    Center_Code = ForeignKey(
        'CenterInfo',
        related_name="groupmappings", on_delete=models.DO_NOTHING
    )

    class Meta:
        ordering = ('-pk',)

    def __unicode__(self):
        return u'%s' % self.GroupMapping_Name

    def __str__(self):
        return u'%s' % self.GroupMapping_Name

    def get_absolute_url(self):
        return reverse('groupmapping_detail', args=(self.pk,))

    def teacher_get_absolute_url(self):
        return reverse('teacher_groupmapping_detail', args=(self.pk,))

    def get_update_url(self):
        return reverse('groupmapping_update', args=(self.pk,))


class InningGroup(models.Model):
    # InningGroup_Name = CharField(max_length=200)
    Use_Flag = BooleanField(default=True)
    Register_DateTime = DateTimeField(auto_now_add=True)
    Updated_DateTime = DateTimeField(auto_now=True)
    Register_Agent = CharField(max_length=500, blank=True, null=True)

    # Relationship Fields
    Course_Code = ForeignKey(
        'CourseInfo',
        related_name="inninggroups", on_delete=models.DO_NOTHING
    )

    Teacher_Code = models.ManyToManyField(
        'MemberInfo'
    )

    Center_Code = ForeignKey(
        'CenterInfo',
        related_name="inninggroups", on_delete=models.DO_NOTHING
    )

    class Meta:
        ordering = ('-pk',)

    def __str__(self):
        return self.Course_Code.Course_Name
        # + " - " + str(self.Teacher_Code.count())

    def __unicode__(self):
        return u'%s' % self.pk

    def get_absolute_url(self):
        return reverse('inninggroup_detail', args=(self.pk,))

    def get_update_url(self):
        return reverse('inninggroup_update', args=(self.pk,))


class InningInfo(models.Model):
    Start_Date = DateTimeField()
    End_Date = DateTimeField()

    Use_Flag = BooleanField(default=True)
    Register_DateTime = DateTimeField(auto_now_add=True)
    Updated_DateTime = DateTimeField(auto_now=True)
    Register_Agent = CharField(max_length=500, blank=True, null=True)

    # Relationship Fields
    Inning_Name = ForeignKey(
        'SessionInfo',
        related_name="inninginfos", on_delete=models.CASCADE
    )

    Center_Code = ForeignKey(
        'CenterInfo',
        related_name="inninginfos", on_delete=models.CASCADE
    )

    Groups = ForeignKey(
        'GroupMapping',
        related_name="inninginfos", on_delete=models.CASCADE
    )

    Course_Group = models.ManyToManyField(
        'InningGroup',
    )

    class Meta:
        ordering = ('-pk',)

    def __unicode__(self):
        return u'%s' % self.pk

    def get_absolute_url(self):
        return reverse('inninginfo_detail', args=(self.pk,))

    def get_teacher_url(self):
        return reverse('teachers_mysession_detail', args=(self.pk,))

    def get_update_url(self):
        return reverse('inninginfo_update', args=(self.pk,))

    def get_teacher_update_url(self):
        return reverse('teachers_inninginfo_update', args=(self.pk,))

    def __str__(self):
        return self.Inning_Name.Session_Name


class MessageInfo(models.Model):
    # Fields
    teacher_code = IntegerField(blank=True, null=True)
    message = CharField(max_length=4000, blank=True, null=True)
    message_read = CharField(max_length=1, blank=True, null=True)

    Use_Flag = BooleanField(default=True)
    Register_DateTime = DateTimeField(auto_now_add=True)
    Updated_DateTime = DateTimeField(auto_now=True)
    Register_Agent = CharField(max_length=500, blank=True, null=True)

    # Relationship Fields
    member_code = ForeignKey(
        'MemberInfo',
        related_name="messageinfos", on_delete=models.DO_NOTHING
    )

    class Meta:
        ordering = ('-pk',)

    def __unicode__(self):
        return u'%s' % self.pk

    def get_absolute_url(self):
        return reverse('messageinfo_detail', args=(self.pk,))

    def get_update_url(self):
        return reverse('messageinfo_update', args=(self.pk,))


class Events(models.Model):
    even_id = models.AutoField(primary_key=True)
    event_name = models.CharField(max_length=255, null=True, blank=True)
    start_date = models.DateTimeField(null=True, blank=True)
    end_date = models.DateTimeField(null=True, blank=True)
    event_type = models.CharField(max_length=10, null=True, blank=True)

    def __str__(self):
        return self.event_name


class InningManager(models.Model):
    sessioninfoobj = models.OneToOneField('InningInfo', on_delete=models.CASCADE)
    memberinfoobj = models.ManyToManyField('MemberInfo', blank=True, null=True)

    def get_absolute_url(self):
        return reverse('mysessions', args=(self.pk,))


class Attendance(models.Model):
    # Fields
    updated = models.DateTimeField(auto_now=True)
    attendance_date = models.DateField(editable=True)
    present = models.BooleanField()

    member_code = ForeignKey(
        'MemberInfo', on_delete=models.CASCADE
    )

    course = ForeignKey(
        'CourseInfo', on_delete=models.CASCADE
    )

    class Meta:
        ordering = ('-attendance_date',)

    def __unicode__(self):
        return u'%s' % self.pk

    def get_absolute_url(self):
        return reverse('teacher_attendance_detail', args=(self.pk,))

    def get_update_url(self):
        return reverse('teacher_attendance_update', args=(self.pk,))
