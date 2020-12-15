from rest_framework import viewsets, permissions
from rest_framework.authentication import SessionAuthentication

from WebApp.student_module.views import Topic_related_to_user
from forum import models, serializers
from forum.models import Thread, Post
from forum.serializers import ThreadSerializer, PostSerializer


class SessionAuthenticationExemptCSRF(SessionAuthentication):

    def enforce_csrf(self, request):
        return


class ThreadViewSet(viewsets.ModelViewSet):
    """ViewSet for the Thread class"""

    queryset = models.Thread.objects.all()
    serializer_class = serializers.ThreadSerializer
    permission_classes = [permissions.IsAuthenticated]


class PostViewSet(viewsets.ModelViewSet):
    """ViewSet for the Post class"""

    queryset = models.Post.objects.all()
    serializer_class = serializers.PostSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_fields = ['thread']


class NotificationViewSet(viewsets.ModelViewSet):
    """ViewSet for the Notification class"""

    queryset = models.Notification.objects.all()
    serializer_class = serializers.NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]


class AppendixViewSet(viewsets.ModelViewSet):
    """ViewSet for the Appendix class"""

    queryset = models.Appendix.objects.all()
    serializer_class = serializers.AppendixSerializer
    permission_classes = [permissions.IsAuthenticated]


class NodeGroupViewSet(viewsets.ModelViewSet):
    """ViewSet for the NodeGroup class"""

    queryset = models.NodeGroup.objects.all()
    serializer_class = serializers.NodeGroupSerializer
    permission_classes = [permissions.IsAuthenticated]


class TopicViewSet(viewsets.ModelViewSet):
    """ViewSet for the Topic class"""

    queryset = models.Topic.objects.all()
    serializer_class = serializers.TopicSerializer
    permission_classes = [permissions.IsAuthenticated]


class ForumAvatarViewSet(viewsets.ModelViewSet):
    """ViewSet for the ForumAvatar class"""

    queryset = models.ForumAvatar.objects.all()
    serializer_class = serializers.ForumAvatarSerializer
    permission_classes = [permissions.IsAuthenticated]


from rest_framework.response import Response


class StudnetTopic(viewsets.ModelViewSet):
    """ViewSet for the ForumAvatar class"""

    queryset = models.Topic.objects.all()
    serializer_class = serializers.TopicSerializer
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request, *args, **kwargs):
        queryset = Topic_related_to_user(request)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
