# -*- coding: utf-8 -*-
from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import Thread, Topic, Post, Appendix, NodeGroup


class PostInline(admin.TabularInline):
    model = Post
    raw_id_fields = (
        'user',
    )
    fields = (
        'user',
        'content_raw',
        'hidden',
    )
    extra = 1


class AppendixInline(admin.TabularInline):
    model = Appendix
    fields = (
        'content_raw',
    )
    extra = 1


class ThreadAdmin(admin.ModelAdmin):

    def is_top_thread(self, obj):
        return obj.order < 10

    is_top_thread.boolean = True

    list_display = (
        'title',
        'user',
        'pub_date',
        'last_replied',
        'view_count',
        'reply_count',
        'hidden',
        'closed',
        'is_top_thread',
    )
    fields = (
        'user',
        'title',
        'content_raw',
        'hidden',
        'closed'
    )

    search_fields = (
        'title',
        'user__username',
        'user__email'
    )
    raw_id_fields = (
        'user',
    )
    inlines = [
        PostInline,
        AppendixInline
    ]


class TopicAdmin(admin.ModelAdmin):

    def number_of_threads(self, obj):
        threads = Thread.objects.filter(topic=obj)
        return "{}({})".format(threads.count(), threads.visible().count())

    number_of_threads.short_description = "Number of Threads [total(visible)]"

    list_display = (
        'id',
        'title',
        'number_of_threads',

    )
    search_fields = (
        'title',
    )


class NodeGroupAdmin(admin.ModelAdmin):

    def number_of_topics(self, obj):
        topics = Topic.objects.filter(node_group=obj)
        return "{}({})".format(topics.count(), topics.count())

    number_of_topics.short_description = "Number of topics [total(visible)]"

    list_display = (
        'title',
        'number_of_topics'
    )
    search_fields = (
        'title',
    )


admin.site.register(Thread, ThreadAdmin)
admin.site.register(NodeGroup, NodeGroupAdmin)
admin.site.register(Topic, TopicAdmin)
