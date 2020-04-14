import json

from django.conf import settings
from rest_framework import generics, status
from rest_framework import viewsets, permissions
from rest_framework.response import Response

from . import models
from . import serializers


class CenterInfoViewSet(viewsets.ModelViewSet):
    """ViewSet for the CenterInfo class"""

    queryset = models.CenterInfo.objects.all()
    serializer_class = serializers.CenterInfoSerializer
    permission_classes = [permissions.IsAuthenticated]


from url_filter.integrations.drf import DjangoFilterBackend


class MemberInfoViewSet(viewsets.ModelViewSet):
    """ViewSet for the MemberInfo class"""

    queryset = models.MemberInfo.objects.all()
    serializer_class = serializers.MemberInfoSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filter_fields = ['id', 'username']


class CourseInfoViewSet(viewsets.ModelViewSet):
    """ViewSet for the CourseInfo class"""

    queryset = models.CourseInfo.objects.all()
    serializer_class = serializers.CourseInfoSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filter_fields = ['id', ]


class ChapterInfoViewSet(viewsets.ModelViewSet):
    """ViewSet for the ChapterInfo class"""

    queryset = models.ChapterInfo.objects.all()
    serializer_class = serializers.ChapterInfoSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filter_fields = ['id', 'Course_Code']


class InningInfoViewSet(viewsets.ModelViewSet):
    """ViewSet for the InningInfo class"""

    queryset = models.InningInfo.objects.all()
    serializer_class = serializers.InningInfoSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filter_fields = ['Groups', ]


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

    queryset = models.AssignmentQuestionInfo.objects.all()
    serializer_class = serializers.QuestionInfoSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = self.queryset
        if self.request.GET.get('Assignment_Code', None):
            query_set = queryset.filter(Assignment_Code=self.request.GET.get('Assignment_Code', None))
        return query_set



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
    filter_backends = [DjangoFilterBackend]
    filter_fields = ['id', ]


class GroupMappingViewSet(viewsets.ModelViewSet):
    """ViewSet for the GroupMapping class"""

    queryset = models.GroupMapping.objects.all()
    serializer_class = serializers.GroupMappingSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filter_fields = ['Students', ]


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


class ChapterContent(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, chapterID):
        if models.ChapterInfo.objects.filter(id=chapterID).exists():
            chapterobj = models.ChapterInfo.objects.get(id=chapterID)
        else:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR, data={'data': 'Chapter does not exist'})
        courseID = chapterobj.Course_Code.id

        path = settings.MEDIA_ROOT
        courseID = chapterobj.Course_Code.id
        try:
            with open(path + '/chapterBuilder/' + str(courseID) + '/' + str(chapterID) + '/' + str(
                    chapterID) + '.txt') as json_file:
                data = json.load(json_file)
        except Exception as e:
            return Response(status=status.HTTP_404_NOT_FOUND, data={'data': 'Chapter File does not exist'})
        return Response(status=status.HTTP_200_OK, data={'data': data})


class AttendanceViewSet(viewsets.ModelViewSet):
    """ViewSet for the Attendance class"""

    queryset = models.Attendance.objects.all()
    serializer_class = serializers.AttendanceSerializer
    permission_classes = [permissions.IsAuthenticated]
