# -*- coding: utf-8 -*-
import re

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.shortcuts import render
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext as _
from django.views.generic import ListView
from textblob import TextBlob

# These views are only for admin. So  AdminAuthMxnCls is used.     AuthCheck(request, admn=1) is used for func based views.
from LMS.auth_views import AdminAuthMxnCls, AuthCheck
from .forms import ThreadForm, ThreadEditForm, AppendixForm, ForumAvatarForm, ReplyForm, TopicForm, TopicEditForm, \
    PostEditForm
from .misc import get_query
from .models import Thread, Topic, Post, Notification, ForumAvatar, NodeGroup

EMAIL_REGEX = re.compile(r"[^@]+@[^@]+\.[^@]+")
User = get_user_model()


def get_default_ordering():
    return getattr(
        settings,
        "forum_DEFAULT_THREAD_ORDERING",
        "-last_replied"
    )


def get_thread_ordering(request):
    query_order = request.GET.get("order", "")
    if query_order in ["-last_replied", "last_replied", "pub_date", "-pub_date"]:
        return query_order
    return get_default_ordering()


def Topic_related_to_user(request):
    return (Topic.objects.filter(center_associated_with=request.user.Center_Code) | Topic.objects.filter(
        center_associated_with__isnull=True))


def Thread_related_to_user(request):
    return Thread.objects.filter(topic__in=Topic_related_to_user(request))


# Create your views here.
class Index(AdminAuthMxnCls, LoginRequiredMixin, ListView):
    model = Thread
    template_name = 'forum/index.html'
    context_object_name = 'threads'

    # def get_queryset(self):
    #     nodegroups = NodeGroup.objects.all()

    #     threadqueryset = Thread.objects.none()
    #     for ng in nodegroups:
    #         thread_counter = 0
    #         topics = Topic.objects.filter(node_group=ng.pk, center_associated_with= self.request.user.Center_Code)
    #         for topic in topics:
    #             thread_counter += topic.thread_count
    #             threads = Thread.objects.visible().filter(topic=topic.pk).order_by('pub_date').filter(
    #                 topic_id__in=Topic_related_to_user(self.request))[:4]

    #             threadqueryset |= threads
    #         if thread_counter == 0:
    #             nodegroups = nodegroups.exclude(pk = ng.pk)
    #     return threadqueryset[:4]

    def get_context_data(self, **kwargs):
        context = super(ListView, self).get_context_data(**kwargs)
        nodegroups = NodeGroup.objects.all()
        threads = []

        for ng in nodegroups:
            thread_counter = 0
            topics = Topic.objects.filter(node_group=ng.pk,
                                          center_associated_with=self.request.user.Center_Code) | Topic.objects.filter(
                node_group=ng.pk, center_associated_with__isnull=True)
            for topic in topics:
                thread_counter += topic.threads_count
            if thread_counter == 0:
                nodegroups = nodegroups.exclude(pk=ng.pk)
            else:
                thread = Thread.objects.filter(topic_id__in=topics).order_by('-pub_date')[:4]
                threads += thread

        context['nodegroups'] = nodegroups
        context['threads'] = threads
        context['panel_title'] = _('New Threads')
        context['title'] = _('Index')
        context['topics'] = Topic.objects.all().filter(id__in=Topic_related_to_user(self.request))
        context['show_order'] = True
        context['get_top_thread_keywords'] = get_top_thread_keywords(self.request, 10)
        return context


class NodeGroupView(AdminAuthMxnCls, LoginRequiredMixin, ListView):
    model = Topic
    template_name = 'forum/nodegroup.html'
    context_object_name = 'topics'

    def get_queryset(self):

        return Topic.objects.filter(
            node_group__id=self.kwargs.get('pk')
        ).select_related(
            'user', 'node_group'
        ).prefetch_related(
            'user__forum_avatar'
        ).filter(id__in=Topic_related_to_user(self.request))

    def get_context_data(self, **kwargs):
        topics = Topic.objects.filter(node_group__id=self.kwargs.get('pk')).filter(
            id__in=Topic_related_to_user(self.request))

        latest_threads = []
        for topic in topics:
            reply_count = 0
            try:
                thread = Thread.objects.filter(
                    topic=topic.pk).order_by('pub_date')[0]
                reply_count = Post.objects.filter(thread=thread.pk).count()

            except:
                thread = None
            latest_threads.append([topic, thread, reply_count])
        context = super(ListView, self).get_context_data(**kwargs)
        context['node_group'] = nodegroup = NodeGroup.objects.get(
            pk=self.kwargs.get('pk'))
        context['title'] = context['panel_title'] = nodegroup.title
        context['show_order'] = True
        context['latest_thread_for_topics'] = latest_threads
        return context


class TopicView(AdminAuthMxnCls, LoginRequiredMixin, ListView):
    model = Thread
    paginate_by = 20
    template_name = 'forum/topic.html'
    context_object_name = 'threads'

    def get_queryset(self):
        return Thread.objects.filter(
            topic__id=self.kwargs.get('pk')
        ).select_related(
            'user', 'topic'
        ).prefetch_related(
            'user__forum_avatar'
        ).order_by(
            *['order', get_thread_ordering(self.request)]
        ).filter(topic_id__in=Topic_related_to_user(self.request))

    def get_context_data(self, **kwargs):
        context = super(ListView, self).get_context_data(**kwargs)
        context['topic'] = topic = Topic.objects.get(pk=self.kwargs.get('pk'))
        context['title'] = context['panel_title'] = topic.title
        context['show_order'] = True
        return context


class ThreadView(AdminAuthMxnCls, LoginRequiredMixin, ListView):
    model = Post
    paginate_by = 15
    template_name = 'forum/thread.html'
    context_object_name = 'posts'

    def get_queryset(self):
        return Post.objects.filter(
            thread_id=self.kwargs.get('pk')
        ).select_related(
            'user'
        ).prefetch_related(
            'user__forum_avatar'
        ).order_by('pub_date')[:5]

    def get_context_data(self, **kwargs):
        context = super(ListView, self).get_context_data(**kwargs)
        current = Thread.objects.get(pk=self.kwargs.get('pk'))
        current.increase_view_count()
        context['thread'] = current
        context['title'] = context['thread'].title
        context['topic'] = context['thread'].topic
        context['form'] = ReplyForm()

        context['total_reply_count'] = Post.objects.filter(
            thread_id=self.kwargs.get('pk')
        ).select_related(
            'user'
        ).prefetch_related(
            'user__forum_avatar'
        ).order_by('pub_date').count()
        return context

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        current = Thread.objects.visible().get(pk=self.kwargs.get('pk'))
        if current.closed:
            return HttpResponseForbidden("Thread closed")
        thread_id = self.kwargs.get('pk')
        form = ReplyForm(
            request.POST,
            user=request.user,
            thread_id=thread_id
        )
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(
                reverse('forum:thread', kwargs={'pk': thread_id})
            )


def ThreadList_LoadMoreViewAjax(request, pk, count):
    AuthCheck(request, admn=1)
    return render(request, 'ForumInclude/LoadMoreAjax.html', {
        'MoreReply': Post.objects.filter(
            thread_id=pk
        ).select_related(
            'user'
        ).prefetch_related(
            'user__forum_avatar'
        ).order_by('pub_date')[5 * count:(1 + count) * 5]

    })


def user_info(request, pk):
    AuthCheck(request, admn=1)
    u = User.objects.get(pk=pk)
    return render(request, 'forum/user_info.html', {
        'title': u.username,
        'user': u,
        'threads': u.threads.visible().select_related('topic')[:10],
        'replies': u.posts.visible().select_related('thread', 'user').order_by('-pub_date')[:30],
    })


class UserThreads(AdminAuthMxnCls, LoginRequiredMixin, ListView):
    model = Post
    paginate_by = 15
    template_name = 'forum/user_threads.html'
    context_object_name = 'threads'

    def get_queryset(self):
        return Thread.objects.filter(
            user_id=self.kwargs.get('pk')
        ).select_related(
            'user', 'topic'
        ).prefetch_related(
            'user__forum_avatar'
        )

    def get_context_data(self, **kwargs):
        context = super(ListView, self).get_context_data(**kwargs)
        context['user'] = User.objects.get(pk=self.kwargs.get('pk'))
        context['panel_title'] = context['title'] = context['user'].username
        return context


class UserPosts(AdminAuthMxnCls, LoginRequiredMixin, ListView):
    model = Post
    paginate_by = 15
    template_name = 'forum/user_replies.html'
    context_object_name = 'replies'

    def get_queryset(self):
        return Post.objects.visible().filter(
            user_id=self.kwargs.get('pk')
        ).select_related(
            'user', 'thread'
        ).prefetch_related(
            'user__forum_avatar'
        )

    def get_context_data(self, **kwargs):
        context = super(ListView, self).get_context_data(**kwargs)
        context['user'] = User.objects.get(pk=self.kwargs.get('pk'))
        context['panel_title'] = context['title'] = context['user'].username
        return context


class SearchView(AdminAuthMxnCls, LoginRequiredMixin, ListView):
    model = Thread
    paginate_by = 10
    template_name = 'forum/search.html'
    context_object_name = 'threads'

    def get_queryset(self):
        keywords = self.kwargs.get('keyword')
        query = get_query(keywords, ['title'])
        return Thread.objects.filter(
            query
        ).select_related(
            'user', 'topic'
        ).prefetch_related(
            'user__forum_avatar'
        ).order_by(
            get_thread_ordering(self.request)
        ).filter(topic_id__in=Topic_related_to_user(self.request))[:100]

    def get_context_data(self, **kwargs):
        context = super(ListView, self).get_context_data(**kwargs)
        context['title'] = context['panel_title'] = _(
            'Search: ') + self.kwargs.get('keyword')
        context['show_order'] = True
        context['keyword'] = self.kwargs.get('keyword')
        return context


def search_redirect(request):
    AuthCheck(request, admn=1)
    if request.method == 'GET':
        keyword = request.GET.get('keyword')
        return HttpResponseRedirect(reverse('forum:search', kwargs={'keyword': keyword}))
    else:
        return HttpResponseForbidden('Post you cannot')


@login_required
def create_thread(request, topic_pk=None, nodegroup_pk=None):
    AuthCheck(request, admn=1)
    topic = None
    topics = Topic.objects.all()
    node_group = NodeGroup.objects.all()
    fixed_nodegroup = NodeGroup.objects.filter(pk=nodegroup_pk)
    if topic_pk:
        topic = Topic.objects.get(pk=topic_pk)
    if nodegroup_pk:
        topics = topics.filter(node_group=nodegroup_pk)
    topics = topics.filter(id__in=Topic_related_to_user(request))
    # print('topics', topics, nodegroup_pk)
    if request.method == 'POST':
        form = ThreadForm(request.POST, user=request.user)

        if form.is_valid():
            t = form.save()
            return HttpResponseRedirect(reverse('forum:thread', kwargs={'pk': t.pk}))
    else:
        form = ThreadForm(user=request.user)

    return render(request, 'forum/create_thread.html',
                  {'form': form, 'node_group': node_group, 'title': _('Create Thread'), 'topic': topic,
                   'fixed_nodegroup': fixed_nodegroup, 'topics': topics})


import operator
from django.db.models import Q
from functools import reduce


def ThreadSearchAjax(request, topic_id, threadkeywordList):
    AuthCheck(request, admn=1)
    threadkeywordList = threadkeywordList.split("_")
    RelevantThread = []
    if topic_id:
        RelevantThread = Thread.objects.filter(topic=topic_id)
        pass
    else:
        RelevantTopics = Topic_related_to_user(request).values_list('pk')
        RelevantThread = Thread.objects.filter(topic__in=RelevantTopics)
        pass
    RelevantThread = RelevantThread.filter(reduce(operator.and_, (Q(title__contains=x) for x in threadkeywordList)))[:5]
    return render(request, 'forum/ThreadSearchAjax.html', {'RelevantThread': RelevantThread})


@login_required
def create_topic(request, nodegroup_pk=None):
    AuthCheck(request, admn=1)
    node_group = NodeGroup.objects.filter(pk=nodegroup_pk)
    if request.method == 'POST':
        form = TopicForm(request.POST, user=request.user)
        if form.is_valid():
            t = form.save()
            return HttpResponseRedirect(reverse('forum:topic', kwargs={'pk': t.pk}))
    else:
        form = TopicForm()

    return render(request, 'forum/create_topic.html',
                  {'form': form, 'title': _('Create Topic'), 'node_group': node_group})


@login_required
def edit_thread(request, pk):
    AuthCheck(request, admn=1)

    thread = Thread.objects.get(pk=pk)
    if thread.reply_count < 0:
        return HttpResponseForbidden(_('Editing is not allowed when thread has been replied'))
    if not thread.user == request.user:
        return HttpResponseForbidden(_('You are not allowed to edit other\'s thread'))
    if request.method == 'POST':
        form = ThreadEditForm(request.POST, instance=thread)
        if form.is_valid():
            t = form.save()
            return HttpResponseRedirect(reverse('forum:thread', kwargs={'pk': t.pk}))
    else:
        form = ThreadEditForm(instance=thread)

    return render(request, 'forum/edit_thread.html', {'form': form, 'object': thread, 'title': ('Edit thread')})


@login_required
def edit_post(request, pk):
    AuthCheck(request, admn=1)
    post = Post.objects.get(pk=pk)
    if not post.user == request.user:
        return HttpResponseForbidden(_('You are not allowed to edit other\'s thread'))
    if request.method == 'POST':
        form = PostEditForm(request.POST, instance=post)
        if form.is_valid():
            t = form.save()
            return HttpResponseRedirect(reverse('forum:thread', kwargs={'pk': t.thread.pk}))
    else:
        form = PostEditForm(instance=post)

    return render(request, 'forum/edit_post.html', {'form': form, 'title': _('Edit Post')})


@login_required
def edit_topic(request, pk):
    AuthCheck(request, admn=1)
    topic = Topic.objects.get(pk=pk)
    if not topic.user == request.user:
        return HttpResponseForbidden(_('You are not allowed to edit other\'s thread'))
    if request.method == 'POST':
        form = TopicEditForm(request.POST, instance=topic)
        if form.is_valid():
            t = form.save()
            return HttpResponseRedirect(reverse('forum:topic', kwargs={'pk': t.pk}))
    else:
        form = TopicEditForm(instance=topic)

    return render(request, 'forum/edit_topic.html', {'form': form, 'title': _('Edit topic')})


@login_required
def create_appendix(request, pk):
    thread = Thread.objects.get(pk=pk)
    if not thread.user == request.user:
        return HttpResponseForbidden(_('You are not allowed to append other\'s thread'))
    if request.method == 'POST':
        form = AppendixForm(request.POST, thread=thread)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('forum:thread', kwargs={'pk': thread.pk}))
    else:
        form = AppendixForm()

    return render(request, 'forum/create_appendix.html', {
        'form': form, 'title': _('Create Appendix'), 'pk': pk
    })


@login_required
def upload_avatar(request):
    avatar = ForumAvatar.objects.filter(user_id=request.user.id).first()
    if request.method == 'POST':
        if avatar:
            form = ForumAvatarForm(
                request.POST, request.FILES, instance=avatar, user=request.user)
        else:
            form = ForumAvatarForm(
                request.POST, request.FILES, user=request.user)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('forum:index'))
    else:
        if avatar:
            form = ForumAvatarForm(instance=request.user.forum_avatar)
        else:
            form = ForumAvatarForm()

    return render(request, 'forum/upload_avatar.html', {'form': form, 'title': _('Upload Avatar')})


@login_required
def notification_view(request):
    notifications = request.user.received_notifications.all().order_by('-pub_date')
    Notification.objects.filter(to=request.user).update(read=True)
    return render(request, 'forum/notifications.html', {
        'title': _("Notifications"),
        'notifications': notifications,
    })


class NotificationView(AdminAuthMxnCls, LoginRequiredMixin, ListView):
    model = Notification
    paginate_by = 20
    template_name = 'forum/notifications.html'
    context_object_name = 'notifications'

    def get_queryset(self):
        Notification.objects.filter(to=self.request.user).update(read=True)
        return Notification.objects.filter(
            to=self.request.user
        ).select_related(
            'sender', 'thread', 'post'
        ).prefetch_related(
            'sender__forum_avatar', 'post__thread'
        ).order_by('-pub_date')

    def get_context_data(self, **kwargs):
        context = super(ListView, self).get_context_data(**kwargs)
        context['title'] = _("Notifications")
        return context


def login_view(request):
    if request.method == "GET":
        return render(request, 'forum/login.html', {'title': _("Login")})
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        valid = True
        if not username or not password:
            valid = False
            messages.add_message(request, messages.INFO, _(
                "Username and password cannot be empty"))
        user = User.objects.filter(username=username).first()
        if not user:
            valid = False
            messages.add_message(request, messages.INFO,
                                 _("User does not exist"))
        user = authenticate(username=username, password=password)
        if (user is not None) and valid:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('forum:index'))
            else:
                valid = False
                messages.add_message(
                    request, messages.INFO, _("User deactivated"))
        else:
            valid = False
            messages.add_message(request, messages.INFO,
                                 _("Incorrect password"))
        if not valid:
            return HttpResponseRedirect(reverse("forum:login"))


def reg_view(request):
    if request.method == "GET":
        return render(request, 'forum/reg.html', {'title': _("Reg")})
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password1")
        password2 = request.POST.get("password2")
        valid = True
        if User.objects.filter(username=username).exists():
            valid = False
            messages.add_message(request, messages.INFO,
                                 _("User already exists"))
        if password != password2:
            valid = False
            messages.add_message(request, messages.INFO,
                                 _("Password does not match"))
        if not EMAIL_REGEX.match(email):
            valid = False
            messages.add_message(request, messages.INFO, _("Invalid Email"))
        if not valid:
            return HttpResponseRedirect(reverse("forum:reg"))
        else:
            User.objects.create_user(
                username=username,
                password=password,
                email=email
            )
            user = authenticate(
                username=username,
                password=password
            )
            login(request, user)
            return HttpResponseRedirect(reverse("forum:index"))


@login_required
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("forum:index"))


def get_top_thread_keywords(request, number_of_keyword):
    obj = Thread.objects.visible().filter(topic__in=Topic_related_to_user(request))
    word_counter = {}
    for eachx in obj:
        words = TextBlob(eachx.title).noun_phrases
        for eachword in words:
            for singleword in eachword.split(" "):
                if singleword in word_counter:
                    word_counter[singleword] += 1
                else:
                    word_counter[singleword] = 1

    popular_words = sorted(word_counter, key=word_counter.get, reverse=True)
    return popular_words[:number_of_keyword]
