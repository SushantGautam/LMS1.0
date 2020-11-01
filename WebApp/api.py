import json

from django.conf import settings
from django.db.models import Q
from django.utils import timezone
from rest_framework import generics, status
from rest_framework import viewsets, permissions
from rest_framework.response import Response

from WebApp.models import AssignmentQuestionInfo
from . import models
from . import serializers


class CenterInfoViewSet(viewsets.ModelViewSet):
    """ViewSet for the CenterInfo class"""

    queryset = models.CenterInfo.objects.all()
    serializer_class = serializers.CenterInfoSerializer
    permission_classes = [permissions.IsAuthenticated]


class SessionMapInfoViewSet(viewsets.ModelViewSet):
    """ViewSet for the CenterInfo class"""

    queryset = models.SessionMapInfo.objects.all()
    serializer_class = serializers.SessionMapInfoSerializer
    permission_classes = [permissions.IsAuthenticated]

    def dispatch(self, request, *args, **kwargs):
        if self.request.GET.get('content'):
            from django.apps import apps
            try:
                self.model = apps.get_model('WebApp', self.request.GET.get("content"))
            except:
                self.model = None
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        if self.request.GET.get('session'):
            self.queryset = self.queryset.filter(Session_Code__pk__in=self.request.GET.get('session').split(','))
        if self.request.GET.get('content'):
            if not self.model:
                from rest_framework.exceptions import NotFound
                raise NotFound

            self.queryset = self.queryset.filter(content_type__model=self.model._meta.model_name)

            if self.request.GET.get('instance'):
                self.queryset = self.queryset.filter(object_id=self.request.GET.get('instance'))

        return self.queryset


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

    def get_queryset(self):
        if self.request.GET.get('course'):
            self.queryset = self.queryset.filter(Course_Code__pk__in=self.request.GET.get('course').split(','))

            if self.request.GET.get('session'):
                from WebApp.student_module.views import student_active_chapters
                self.queryset = student_active_chapters(self.request.GET.get('course').split(','),
                                                        self.request.GET.get('session').split(','))

        return self.queryset


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
            queryset = queryset.filter(Assignment_Code__pk=self.request.GET.get('Assignment_Code', None))
        return queryset


class AssignAnswerInfoViewSet(viewsets.ModelViewSet):
    """ViewSet for the AssignAnswerInfo class"""

    queryset = models.AssignAnswerInfo.objects.all()
    serializer_class = serializers.AssignAnswerInfoSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = self.queryset
        user_id = self.request.GET.get('Student_Code', None)
        question_id = self.request.GET.get('Question_Code', None)
        assignment_id = self.request.GET.get('Assignment_Code', None)
        if assignment_id:
            queryset = queryset.filter(
                Question_Code__in=AssignmentQuestionInfo.objects.filter(Assignment_Code__pk=assignment_id)
            )
        if user_id:
            queryset = queryset.filter(Student_Code__pk=user_id)
        if question_id:
            queryset = queryset.filter(Question_Code__pk=question_id)
        return queryset


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

    def get_serializer_context(self):
        context = super(AssignmentInfoViewSet, self).get_serializer_context()
        context.update({"request": self.request})
        return context

    def get_queryset(self):
        queryset = self.queryset.filter(Course_Code__Center_Code=self.request.user.Center_Code)
        datetime_now = timezone.now().replace(microsecond=0)
        if 'Course_Code' in self.request.GET:
            if self.request.GET.get('Course_Code'):
                queryset = queryset.filter(
                    Course_Code__in=self.request.GET.get('Course_Code').split(','), Chapter_Code__Use_Flag=True,
                    Assignment_Start__lte=datetime_now
                ).filter(
                    Q(Chapter_Code__Start_Date__lte=datetime_now) | Q(Chapter_Code__Start_Date=None)).filter(
                    Q(Chapter_Code__End_Date__gte=datetime_now) | Q(Chapter_Code__End_Date=None)
                )
            else:
                queryset = ''
        if self.request.GET.get('active'):
            if self.request.GET.get('active') == '1':
                queryset = queryset.filter(Assignment_Start__lte=datetime_now, Assignment_Deadline__gte=datetime_now)
        if self.request.GET.get('expired'):
            if self.request.GET.get('expired') == '1':
                queryset = queryset.filter(Assignment_Deadline__lte=datetime_now)
        return queryset


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
            # return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR, data={'data': 'Chapter does not exist'})
            return Response(status=status.HTTP_200_OK, data={'data': 'Chapter does not exist'})
        courseID = chapterobj.Course_Code.id

        path = settings.MEDIA_ROOT
        courseID = chapterobj.Course_Code.id
        try:
            with open(path + '/chapterBuilder/' + str(courseID) + '/' + str(chapterID) + '/' + str(
                    chapterID) + '.txt') as json_file:
                data = json.load(json_file)
        except Exception as e:
            # return Response(status=status.HTTP_404_NOT_FOUND, data={'data': 'Chapter File does not exist'})
            return Response(status=status.HTTP_200_OK, data={'data': 'Chapter File does not exist'})
        return Response(status=status.HTTP_200_OK, data={'data': data})


class AttendanceViewSet(viewsets.ModelViewSet):
    """ViewSet for the Attendance class"""

    queryset = models.Attendance.objects.all()
    serializer_class = serializers.AttendanceSerializer
    permission_classes = [permissions.IsAuthenticated]
