from django.contrib.auth.models import AbstractUser
from django.contrib.contenttypes.models import ContentType
from django.db import models as models
from django.db.models import ForeignKey, CharField, IntegerField, DateTimeField, BooleanField, \
    ImageField
from django.urls import reverse

from WebApp.models import MemberInfo, InningInfo, CourseInfo, CenterInfo


class CategoryInfo(models.Model):
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
    Survey_Title = CharField(max_length=500)
    Start_Date = DateTimeField(auto_now=False, auto_now_add=False, null=True)
    End_Date = DateTimeField(auto_now=False, auto_now_add=False, null=True)
    Survey_Cover = ImageField(upload_to="Survey_Covers/", blank=True, null=True)
    Use_Flag = BooleanField(default=True)
    Retaken_From = IntegerField(blank=True, null=True,
                                help_text="Store id of previous survey from which it was retaken")
    Version_No = IntegerField(default=1, help_text="To maintain the versioning of the survey")
    Created_Date = DateTimeField(auto_now_add=True)
    Updated_Date = DateTimeField(auto_now=True)
    Survey_Live = BooleanField(default=False, blank=True, null=True)

    Center_Code = ForeignKey(
        'WebApp.CenterInfo',
        related_name="surveyinfo", on_delete=models.DO_NOTHING
    )

    Category_Code = ForeignKey(
        'CategoryInfo',
        related_name="surveyinfo", on_delete=models.DO_NOTHING, default="General"
    )

    Session_Code = ForeignKey(
        'WebApp.InningInfo', blank=True,
        related_name="surveyinfo", on_delete=models.DO_NOTHING, null=True
    )
    Course_Code = ForeignKey(
        'WebApp.CourseInfo', blank=True,
        related_name="surveyinfo", on_delete=models.DO_NOTHING, null=True
    )

    Added_By = ForeignKey(
        'WebApp.MemberInfo',
        related_name="surveyinfo", on_delete=models.DO_NOTHING
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
        return reverse('surveyinfo_retake_ajax', args=(self.pk,))

    def get_create_url(self):
        return reverse('surveyinfo_ajax', args=(self.pk,))


class QuestionInfo(models.Model):
    QUESTION_TYPE_CHOICES = [
        ('SAQ', 'Short Answer'),
        ('MCQ', 'Multiple Choice'),
    ]

    Question_Name = CharField(max_length=500)
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
    Option_Name = CharField(max_length=500)
    Vote_Count = IntegerField(default=0)
    Question_Code = ForeignKey(
        'QuestionInfo',
        related_name="optioninfo", on_delete=models.CASCADE
    )

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

    def get_option_percentage(self):
        total_option = self.Question_Code.answerinfo.all().count()
        selected_option = self.Question_Code.answerinfo.all().filter(Answer_Value=self.id).count()

        if total_option != 0:
            option_percentage = (selected_option * 100) / total_option
        else:
            option_percentage = 0
        return option_percentage


class SubmitSurvey(models.Model):
    Created_Date = DateTimeField(auto_now_add=True)
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
    Answer_Value = CharField(max_length=500, blank=True, null=True)
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
