import html

from django.utils.functional import empty
from rest_framework import serializers

from forum import models


class ThreadQuerysetSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ThreadQueryset
        fields = (
            'pk',
        )


class ThreadSerializer(serializers.ModelSerializer):
    nodegroup = serializers.ReadOnlyField(source='topic.node_group.pk')
    user_name = serializers.ReadOnlyField(source='user.__str__')
    topic_title = serializers.ReadOnlyField(source='topic.title')
    nodegroup_title = serializers.ReadOnlyField(source='topic.node_group.title')
    user_avatar = serializers.ReadOnlyField(source='user.Avatar')

    class Meta:
        model = models.Thread
        fields = (
            'pk',
            'title',
            'content_raw',
            'content_rendered',
            'user',
            'topic',
            'view_count',
            'reply_count',
            'pub_date',
            'last_replied',
            'order',
            'hidden',
            'closed',
            'nodegroup',
            "user_name",
            "topic_title",
            "nodegroup_title",
            "user_avatar",
        )


class PostSerializer(serializers.ModelSerializer):
    user_avatar = serializers.ReadOnlyField(source='user.Avatar')
    user_name = serializers.ReadOnlyField(source='user.__str__')

    class Meta:
        model = models.Post
        fields = (
            'pk',
            'thread',
            'user',
            'content_raw',
            'content_rendered',
            'pub_date',
            'hidden',
            'thread',
            'user',
            'user_avatar',
            'user_name',
        )


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Notification
        fields = (
            'pk',
            'sender',
            'to',
            'post',
            'read',
            'pub_date',
        )


class AppendixSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Appendix
        fields = (
            'pk',
            'pub_date',
            'content_raw',
            'content_rendered',
        )


class NodeGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.NodeGroup
        fields = (
            'pk',
            'title',
            'description',
            'topic_count',
        )


class TopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Topic
        fields = (
            'pk',
            'title',
            'description',
            'thread_count',
            'node_group',
            'topic_icon',
        )


class ForumAvatarSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ForumAvatar
        fields = (
            'pk',
            'use_gravatar',
            'image',
        )
