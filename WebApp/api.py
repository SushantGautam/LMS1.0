from rest_framework import viewsets, permissions

from . import models
from . import serializers


class CenterInfoViewSet(viewsets.ModelViewSet):
    """ViewSet for the CenterInfo class"""

    queryset = models.CenterInfo.objects.all()
    serializer_class = serializers.CenterInfoSerializer
    permission_classes = [permissions.IsAuthenticated]


class MemberInfoViewSet(viewsets.ModelViewSet):
    """ViewSet for the MemberInfo class"""

    queryset = models.MemberInfo.objects.all()
    serializer_class = serializers.MemberInfoSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = ('id', 'username')


class CourseInfoViewSet(viewsets.ModelViewSet):
    """ViewSet for the CourseInfo class"""

    queryset = models.CourseInfo.objects.all()
    serializer_class = serializers.CourseInfoSerializer
    permission_classes = [permissions.IsAuthenticated]


class ChapterInfoViewSet(viewsets.ModelViewSet):
    """ViewSet for the ChapterInfo class"""

    queryset = models.ChapterInfo.objects.all()
    serializer_class = serializers.ChapterInfoSerializer
    permission_classes = [permissions.IsAuthenticated]


class InningInfoViewSet(viewsets.ModelViewSet):
    """ViewSet for the InningInfo class"""

    queryset = models.InningInfo.objects.all()
    serializer_class = serializers.InningInfoSerializer
    permission_classes = [permissions.IsAuthenticated]


class SessionInfoViewSet(viewsets.ModelViewSet):
    """ViewSet for the InningInfo class"""

    queryset = models.SessionInfo.objects.all()
    serializer_class = serializers.SessionInfoSerializer
    permission_classes = [permissions.IsAuthenticated]


class AssignAssignmentInfoViewSet(viewsets.ModelViewSet):
    """ViewSet for the AssignHomeworkInfo class"""

    queryset = models.AssignAssignmentInfo.objects.all()
    serializer_class = serializers.AssignAssignmentInfoSerializer
    permission_classes = [permissions.IsAuthenticated]


class QuestionInfoViewSet(viewsets.ModelViewSet):
    """ViewSet for the QuestionInfo class"""

    queryset = models.QuestionInfo.objects.all()
    serializer_class = serializers.QuestionInfoSerializer
    permission_classes = [permissions.IsAuthenticated]


class AssignAnswerInfoViewSet(viewsets.ModelViewSet):
    """ViewSet for the AssignAnswerInfo class"""

    queryset = models.AssignAnswerInfo.objects.all()
    serializer_class = serializers.AssignAnswerInfoSerializer
    permission_classes = [permissions.IsAuthenticated]

class InningGroupViewSet(viewsets.ModelViewSet):
    """ViewSet for the InningGroup class"""

    queryset = models.InningGroup.objects.all()
    serializer_class = serializers.InningGroupSerializer
    permission_classes = [permissions.IsAuthenticated]


class GroupMappingViewSet(viewsets.ModelViewSet):
    """ViewSet for the GroupMapping class"""

    queryset = models.GroupMapping.objects.all()
    serializer_class = serializers.GroupMappingSerializer
    permission_classes = [permissions.IsAuthenticated]


class AssignmentInfoViewSet(viewsets.ModelViewSet):
    """ViewSet for the HomeworkInfo class"""

    queryset = models.AssignmentInfo.objects.all()
    serializer_class = serializers.AssignmentInfoSerializer
    permission_classes = [permissions.IsAuthenticated]


class MessageInfoViewSet(viewsets.ModelViewSet):
    """ViewSet for the MessageInfo class"""

    queryset = models.MessageInfo.objects.all()
    serializer_class = serializers.MessageInfoSerializer
    permission_classes = [permissions.IsAuthenticated]
