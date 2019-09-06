from . import models
from . import serializers
from rest_framework import viewsets, permissions


class QuizViewSet(viewsets.ModelViewSet):
    """ViewSet for the CategoryInfo class"""

    queryset = models.Quiz.objects.all()
    serializer_class = serializers.QuizSerializer
    permission_classes = [permissions.IsAuthenticated]


class MCQuestionViewSet(viewsets.ModelViewSet):
    """ViewSet for the SurveyInfo class"""

    queryset = models.MCQuestion.objects.all()
    serializer_class = serializers.MCQuestionSerializer
    permission_classes = [permissions.IsAuthenticated]


class TFQuestionViewSet(viewsets.ModelViewSet):
    """ViewSet for the QuestionInfo class"""

    queryset = models.TF_Question.objects.all()
    serializer_class = serializers.TF_QuestionSerializer
    permission_classes = [permissions.IsAuthenticated]

class SAQuestionViewSet(viewsets.ModelViewSet):
    queryset = models.SA_Question.objects.all()
    serializer_class = serializers.SA_QuestionSerializer
    permission_classes = [permissions.IsAuthenticated]


class AnswerViewSet(viewsets.ModelViewSet):
    """ViewSet for the OptionInfo class"""
    queryset = models.Answer.objects.all()
    serializer_class = serializers.AnswerSerializer
    permission_classes = [permissions.IsAuthenticated]

class ProgressViewSet(viewsets.ModelViewSet):
    """ViewSet for the OptionInfo class"""
    queryset = models.Progress.objects.all()
    serializer_class = serializers.ProgressSerializer
    permission_classes = [permissions.IsAuthenticated]

class SittingViewSet(viewsets.ModelViewSet):
    """ViewSet for the OptionInfo class"""
    queryset = models.Sitting.objects.all()
    serializer_class = serializers.SittingSerializer
    permission_classes = [permissions.IsAuthenticated]

