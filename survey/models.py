from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.contrib.contenttypes.models import ContentType
from django.core.files.storage import FileSystemStorage
from django.db import models as models
from django.db.models import ForeignKey, CharField, IntegerField, DateTimeField, TextField, BooleanField, \
    ImageField, DateField, Count
from django.urls import reverse
from django.utils.translation import gettext as _
from WebApp.models import MemberInfo, InningInfo, CourseInfo, CenterInfo


class CategoryInfo(models.Model):

    # Fields
    Category_Name = CharField(max_length=100, blank=True, null=True)
    Category_Icon = CharField(max_length=50, blank=True, null=True)

    class Meta:
        ordering = ('-pk',)

    def __unicode__(self):
        return u'%s' % self.pk

    def __str__(self):
        return self.Category_Name

    def get_absolute_url(self):
        return reverse('categoryinfo_detail', args=(self.pk,))

    def get_update_url(self):
        return reverse('categoryinfo_update', args=(self.pk,))


class SurveyInfo(models.Model):

    # Fields
    Survey_Title = CharField(max_length=500, blank=True, null=True)
    Start_Date = DateField(auto_now=False, auto_now_add=False, null=True)
    End_Date = DateField(auto_now=False, auto_now_add=False, null=True)
    Survey_Cover = ImageField(
        upload_to="Survey_Covers/", blank=True, null=True)
    Use_Flag = BooleanField(default=True)

    Center_Code = ForeignKey(
        'WebApp.CenterInfo',
        related_name="surveyinfo", on_delete=models.DO_NOTHING, null=True
    )

    Session_Code = ForeignKey(
        'WebApp.InningInfo',
        related_name="surveyinfo", on_delete=models.DO_NOTHING, null=True
    )
    Added_By = ForeignKey(
        'WebApp.MemberInfo',
        related_name="surveyinfo", on_delete=models.DO_NOTHING, null=True
    )
    Category_Code = ForeignKey(
        'CategoryInfo',
        related_name="surveyinfo", on_delete=models.DO_NOTHING, null=True
    )
    
    Course_Code = ForeignKey(
        'WebApp.CourseInfo',
        related_name="surveyinfo", on_delete=models.DO_NOTHING, null=True
    )

    class Meta:
        ordering = ('-pk',)

    def __unicode__(self):
        return u'%s' % self.pk

    def __str__(self):      
        return self.Survey_Title

    def questions_count(self):
        return QuestionInfo.objects.filter(Survey_Code=self.pk).count()

    def get_absolute_url(self):
        return reverse('surveyinfo_detail', args=(self.pk,))

    def get_update_url(self):
        return reverse('surveyinfo_update', args=(self.pk,))


class QuestionInfo(models.Model):

    QUESTION_TYPE_CHOICES = [
    ('SAQ', 'Short Answer'),
    ('MCQ', 'Multiple Choice'),
    ]

    # Fields
    Question_Name = CharField(max_length=500, blank=True, null=True)
    # Question_Answer = CharField(max_length=500, blank=True, null=True)
    Question_Type = CharField(max_length=3, choices=QUESTION_TYPE_CHOICES, default='SAQ')
    Survey_Code = ForeignKey(
        'SurveyInfo',
        related_name="questioninfo", on_delete=models.CASCADE
    )

    class Meta:
        ordering = ('-pk',)

    def __unicode__(self):
        return u'%s' % self.pk

    def __str__(self):
        return self.Question_Name

    @property
    def get_answers(self):
        answers = AnswerInfo.objects.all().filter(Question_Code=self.pk).exclude(
            Answer_Value__isnull=True)[:4]

        return answers

    def get_absolute_url(self):
        return reverse('questioninfo_detail', args=(self.pk,))

    def get_update_url(self):
        return reverse('questioninfo_update', args=(self.pk,))


class OptionInfo(models.Model):

    # Fields
    Option_Name = CharField(max_length=500, blank=True, null=True)
    Question_Code = ForeignKey(
        'QuestionInfo',
        related_name="optioninfo", on_delete=models.CASCADE
    )
    # Selected_By = models.ManyToManyField(
    #     MemberInfo,
    #     on_delete=models.CASCADE
    # )

    class Meta:
        ordering = ('-pk',)

    def __unicode__(self):
        return u'%s' % self.pk

    def __str__(self):
        return self.Option_Name

    def get_absolute_url(self):
        return reverse('optioninfo_detail', args=(self.pk,))

    def get_update_url(self):
        return reverse('optioninfo_update', args=(self.pk,))


class SubmitSurvey(models.Model):

    # Fields
    Survey_Code = ForeignKey(
        'SurveyInfo',
        related_name="submitsurvey", on_delete=models.CASCADE
    )
    Student_Code = ForeignKey(
        'WebApp.MemberInfo',
        related_name="submitsurvey", on_delete=models.DO_NOTHING
    )

    class Meta:
        ordering = ('-pk',)

    def __unicode__(self):
        return u'%s' % self.pk

    def get_absolute_url(self):
        return reverse('submitsurvey_detail', args=(self.pk,))

    def get_update_url(self):
        return reverse('submitsurvey_update', args=(self.pk,))


class AnswerInfo(models.Model):

    # Fields
    Answer_Value = CharField(max_length=500, blank=True, null=True)
    # Created_Date = DateTimeField(auto_now_add=True)
    Question_Code = ForeignKey(
        'QuestionInfo',
        related_name="answerinfo", on_delete=models.CASCADE
    )
    Submit_Code = ForeignKey(
        'SubmitSurvey',
        related_name="answerinfo", on_delete=models.CASCADE, 
        null=True,
    )

    class Meta:
        ordering = ('-pk',)

    def __unicode__(self):
        return u'%s' % self.pk

    def get_absolute_url(self):
        return reverse('answerinfo_detail', args=(self.pk,))

    def get_update_url(self):
        return reverse('answerinfo_update', args=(self.pk,))

