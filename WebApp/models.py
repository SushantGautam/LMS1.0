from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.contrib.contenttypes.models import ContentType
from django.core.files.storage import FileSystemStorage
from django.db import models as models
from django.db.models import ForeignKey, CharField, IntegerField, DateTimeField, TextField, BooleanField, ImageField, FileField
from django.urls import reverse
from django.utils.translation import gettext as _

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
        _('username'),
        max_length=150,
        unique=True,
        help_text=_('Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only. Used for login'),
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
        default=False,
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

    Member_ID = models.CharField(max_length=150, blank=True, null=True, help_text=_('ID assigned by university/Roll No'))
    password = models.CharField(_('password'), max_length=264)
    Member_Permanent_Address = models.CharField(max_length=500, blank=True, null=True)
    Member_Temporary_Address = models.CharField(max_length=500, blank=True, null=True)
    Member_BirthDate = models.DateTimeField(blank=True, null=True)
    Member_Phone = models.CharField(max_length=150, blank=True, null=True)
    Use_Flag = BooleanField(default=True)
    Register_DateTime = DateTimeField(auto_now_add=True)
    Register_Agent = CharField(max_length=128, blank=True, null=True)
    Updated_DateTime = DateTimeField(auto_now=True)
    Member_Memo = models.CharField(max_length=500, blank=True, null=True)
    Member_Avatar = models.ImageField(upload_to="Member_images/", blank=True, null=True)
    Is_Teacher = models.BooleanField(default=False)
    Is_Student = models.BooleanField(default=True)
    Is_CenterAdmin = models.BooleanField(default=False)
    Is_Parent = models.BooleanField(default=False)
    Member_Gender = models.CharField(max_length=1, choices=Gender_Choices)

    @property
    def Avatar(self):

        if self.Member_Avatar:
            return self.Member_Avatar.url
        else:
            if self.Member_Gender =='F':
                default_avatar = "/static/images/profile/female.png"
            elif self.Member_Gender =='M':
                default_avatar = "/static/images/profile/male.jpg"
            else:
                default_avatar = "/static/images/profile/profile.png"
            return default_avatar

    # Relationship Fields
    Center_Code = ForeignKey(
        'CenterInfo',
        related_name="memberinfos", on_delete=models.DO_NOTHING, null=True
    )

    class Meta:
        ordering = ('-pk',)

    def __unicode__(self):
        return u'%s' % self.pk

    def get_absolute_url(self):
        return reverse('memberinfo_detail', args=(self.pk,))

    def get_update_url(self):
        return reverse('memberinfo_update', args=(self.pk,))

    # def create_user(self, username, email=None, password=None, **extra_fields):
    #     extra_fields.setdefault('is_staff', True)
    #     extra_fields.setdefault('is_superuser', True)
    #     return self._create_user(username, email, password, **extra_fields)


class CourseInfo(models.Model):
    Course_Name = CharField(max_length=500)
    Course_Description = TextField(blank=True, null=True)
    Course_Cover_File = ImageField(upload_to="Course_images/", blank=True, null=True)
    Course_Level = IntegerField(blank=True, null=True)
    Course_Info = TextField(blank=True, null=True)

    Use_Flag = BooleanField(default=True,  verbose_name="Tick this flag if you want to prevent user from login.")
    Register_DateTime = DateTimeField(auto_now_add=True)
    Updated_DateTime = DateTimeField(auto_now=True)
    Register_Agent = CharField(max_length=500, blank=True, null=True)

    Course_Provider = CharField(max_length=250)

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

    def __str__(self):
        return self.Course_Name


class ChapterInfo(models.Model):
    Chapter_No = IntegerField()
    Chapter_Name = CharField(max_length=200)
    Summary = TextField(blank=True, null=True)
    Page_Num = IntegerField(blank=True, null=True)

    Use_Flag = BooleanField(default=True)
    Register_DateTime = DateTimeField(auto_now_add=True)
    Updated_DateTime = DateTimeField(auto_now=True)
    Register_Agent = CharField(max_length=500, blank=True, null=True)

    # Relationship Fields
    Course_Code = ForeignKey(
        'CourseInfo',
        related_name="chapterinfos", on_delete=models.DO_NOTHING
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

    def __str__(self):
        return self.Chapter_Name


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


#================AssignmentModels================#
class AssignmentInfo(models.Model):
    Assignment_Topic = CharField(max_length=500, blank=True, null=True)
    Use_Flag = BooleanField(default=True)
    Register_DateTime = DateTimeField(auto_now_add=True)
    Updated_DateTime = DateTimeField(auto_now=True)
    Assignment_Deadline = DateTimeField(null=True, blank=True)
    Course_Code = ForeignKey(
        'CourseInfo',
        related_name="assignmentinfos", on_delete=models.DO_NOTHING
    )
    Chapter_Code = ForeignKey(
        'ChapterInfo',
        related_name="assignmentinfos", on_delete=models.DO_NOTHING
    )
    Register_Agent = ForeignKey(
        'MemberInfo',
        related_name="assignmentinfos", on_delete=models.DO_NOTHING
    )

    def __str__(self):
        return self.Assignment_Topic

    def student_get_absolute_url(self):
        return reverse('student_assignmentinfo_detail', args=(self.Course_Code.id, self.Chapter_Code.id, self.pk,))

    def teacher_get_absolute_url(self):
        return reverse('teacher_assignmentinfo_detail', args=(self.Course_Code.id, self.Chapter_Code.id, self.pk,))

    def get_absolute_url(self):
        return reverse('assignmentinfo_detail', args=(self.Course_Code.id, self.Chapter_Code.id, self.pk,))

    def get_update_url(self):
        return reverse('assignmentinfo_update', args=(self.Course_Code.id, self.Chapter_Code.id, self.pk,))


def upload_to(instance, filename):
    return 'questions/{0}/{1}'.format(instance.id, filename)


class AssignmentQuestionInfo(models.Model):
    
    Question_Title = CharField(max_length=4000)
    Question_Score = IntegerField(blank=True, null=True)
    Use_Flag = BooleanField(default=True)
    Register_DateTime = DateTimeField(auto_now_add=True)
    Updated_DateTime = DateTimeField(auto_now=True)

    Question_Media_File = FileField(upload_to=upload_to, blank=True, null=True)
    Question_Description = TextField()
    Answer_Choices = (
        ('S', 'Short Answer'),
        ('F', 'File Upload'),
    )
    Answer_Type = CharField(max_length=1, choices=Answer_Choices)

    Assignment_Code = ForeignKey(
        'AssignmentInfo',
        related_name="questioninfos", on_delete=models.DO_NOTHING
    )

    Register_Agent = ForeignKey(
        'MemberInfo',
        related_name="questioninfos", on_delete=models.DO_NOTHING
    )

    class Meta:
        ordering = ('pk',)

    def __unicode__(self):
        return u'%s' % self.pk

    def get_absolute_url(self):
        return reverse('webapp_questioninfo_detail', args=(self.Assignment_Code.Course_Code.pk,self.Assignment_Code.Chapter_Code.pk,self.Assignment_Code.pk,self.pk))

    def get_update_url(self):
        return reverse('webapp_questioninfo_update', args=(self.Assignment_Code.Course_Code.pk,self.Assignment_Code.Chapter_Code.pk,self.Assignment_Code.pk,self.pk))


class AssignAssignmentInfo(models.Model):
    Use_Flag = BooleanField(default=True)
    Register_DateTime = DateTimeField(auto_now_add=True)
    Updated_DateTime = DateTimeField(auto_now=True)

    # Relationship Fields
    Inning_Code = ForeignKey(
        'InningInfo',
        related_name="assignassignmentinfos", on_delete=models.DO_NOTHING
    )
    Assignment_Code = ForeignKey(
        'AssignmentInfo',
        related_name="assignassignmentinfos", on_delete=models.DO_NOTHING
    )
    Assigned_By = ForeignKey(
        'MemberInfo',
        related_name="assignassignmentinfos", on_delete=models.DO_NOTHING
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
    return 'assignments/{0}/{1}'.format(instance.Assignment_Code.id, filename)


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
        related_name="assignanswerinfos", on_delete=models.DO_NOTHING
    )
    Student_Code = ForeignKey(
        'MemberInfo',
        related_name="assignanswerinfos", on_delete=models.DO_NOTHING
    )

    class Meta:
        ordering = ('-pk',)

    def __unicode__(self):
        return u'%s' % self.pk

    def get_absolute_url(self):
        return reverse('assignanswerinfo_detail', args=(self.pk,))

    def get_update_url(self):
        return reverse('assignanswerinfo_update', args=(self.pk,))

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
        related_name="inninginfos", on_delete=models.DO_NOTHING
    )

    Center_Code = ForeignKey(
        'CenterInfo',
        related_name="inninginfos", on_delete=models.DO_NOTHING
    )

    Groups = ForeignKey(
        'GroupMapping',
        related_name="inninginfos", on_delete=models.DO_NOTHING
    )

    Course_Group = models.ManyToManyField(
        'InningGroup'
    )

    class Meta:
        ordering = ('-pk',)

    def __unicode__(self):
        return u'%s' % self.pk

    def get_absolute_url(self):
        return reverse('inninginfo_detail', args=(self.pk,))

    def get_update_url(self):
        return reverse('inninginfo_update', args=(self.pk,))

    # def __str__(self):
    #     return self.Inning_Name

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


