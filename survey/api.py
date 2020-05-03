from rest_framework import viewsets, permissions
from rest_framework.viewsets import ReadOnlyModelViewSet

from survey.filters import SurveyFilter
from . import models
from . import serializers


class CategoryInfoViewSet(viewsets.ModelViewSet):
    """ViewSet for the CategoryInfo class"""

    queryset = models.CategoryInfo.objects.all()
    serializer_class = serializers.CategoryInfoSerializer
    permission_classes = [permissions.IsAuthenticated]


class SurveyInfoViewSet(ReadOnlyModelViewSet):
    """ViewSet for the SurveyInfo class"""
    filter_class = SurveyFilter
    queryset = models.SurveyInfo.objects.all()
    serializer_class = serializers.SurveyInfoSerializer
    permission_classes = [permissions.IsAuthenticated]


class QuestionInfoViewSet(viewsets.ModelViewSet):
    """ViewSet for the QuestionInfo class"""

    queryset = models.QuestionInfo.objects.all()
    serializer_class = serializers.QuestionInfoSerializer
    permission_classes = [permissions.IsAuthenticated]


class OptionInfoViewSet(viewsets.ModelViewSet):
    """ViewSet for the OptionInfo class"""

    queryset = models.OptionInfo.objects.all()
    serializer_class = serializers.OptionInfoSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_fields = ['Question_Code']


class SubmitSurveyViewSet(viewsets.ModelViewSet):
    """ViewSet for the SubmitSurvey class"""

    queryset = models.SubmitSurvey.objects.all()
    serializer_class = serializers.SubmitSurveySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = self.queryset
        survey_id = self.request.GET.get('Survey_Code', None)
        student_id = self.request.GET.get('Student_Code', None)
        if survey_id:
            queryset = queryset.filter(Survey_Code__pk=survey_id)
        if student_id:
            queryset = queryset.filter(Student_Code__pk=student_id)
        return queryset


class AnswerInfoViewSet(viewsets.ModelViewSet):
    """ViewSet for the AnswerInfo class"""

    queryset = models.AnswerInfo.objects.all()
    serializer_class = serializers.AnswerInfoSerializer
    permission_classes = [permissions.IsAuthenticated]