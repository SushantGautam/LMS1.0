from . import models
from . import serializers
from rest_framework import viewsets, permissions


class CategoryInfoViewSet(viewsets.ModelViewSet):
    """ViewSet for the CategoryInfo class"""

    queryset = models.CategoryInfo.objects.all()
    serializer_class = serializers.CategoryInfoSerializer
    permission_classes = [permissions.IsAuthenticated]


class SurveyInfoViewSet(viewsets.ModelViewSet):
    """ViewSet for the SurveyInfo class"""

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


class SubmitSurveyViewSet(viewsets.ModelViewSet):
    """ViewSet for the SubmitSurvey class"""

    queryset = models.SubmitSurvey.objects.all()
    serializer_class = serializers.SubmitSurveySerializer
    permission_classes = [permissions.IsAuthenticated]


class AnswerInfoViewSet(viewsets.ModelViewSet):
    """ViewSet for the AnswerInfo class"""

    queryset = models.AnswerInfo.objects.all()
    serializer_class = serializers.AnswerInfoSerializer
    permission_classes = [permissions.IsAuthenticated]


