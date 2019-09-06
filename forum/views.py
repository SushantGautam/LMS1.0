# -*- coding: utf-8 -*-
import re

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.shortcuts import render
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext as _
from django.views.generic import ListView
from textblob import TextBlob


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


# Create your views here.
class Index(ListView):
    model = Thread
    template_name = 'forum/index.html'
    context_object_name = 'threads'

    def get_queryset(self):
        nodegroups = NodeGroup.objects.all()
        threadqueryset = Thread.objects.none()
        for ng in nodegroups:
            topics = Topic.objects.filter(node_group=ng.pk)
            for topic in topics:
                threads = Thread.objects.visible().filter(
                    topic=topic.pk).order_by('pub_date')[:4]
                threadqueryset |= threads

        return threadqueryset

    def get_context_data(self, **kwargs):
        context = super(ListView, self).get_context_data(**kwargs)
        context['panel_title'] = _('New Threads')
        context['title'] = _('Index')
        context['topics'] = Topic.objects.all()
        context['show_order'] = True
        context['get_top_thread_keywords'] = get_top_thread_keywords(
            self.request, 10)
        return context


class NodeGroupView(ListView):
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
        )

    def get_context_data(self, **kwargs):
        topics = Topic.objects.filter(node_group__id=self.kwargs.get('pk'))
        latest_threads = []
        for topic in topics:
            reply_count = 0
            try:
                thread = Thread.objects.filter(
                    topic=topic.pk).order_by('pub_date')[0]
                reply_count = Thread.objects.filter(topic=topic.pk).aggregate(
                    Sum('reply_count'))['reply_count__sum']
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


class TopicView(ListView):
    model = Thread
    paginate_by = 20
    template_name = 'forum/topic.html'
    context_object_name = 'threads'

    def get_queryset(self):
        return Thread.objects.visible().filter(
            topic__id=self.kwargs.get('pk')
        ).select_related(
            'user', 'topic'
        ).prefetch_related(
            'user__forum_avatar'
        ).order_by(
            *['order', get_thread_ordering(self.request)]
        )

    def get_context_data(self, **kwargs):
        context = super(ListView, self).get_context_data(**kwargs)
        print(self.kwargs.get('pk'))
        context['topic'] = topic = Topic.objects.get(pk=self.kwargs.get('pk'))
        context['title'] = context['panel_title'] = topic.title
        context['show_order'] = True
        return context


class ThreadView(ListView):
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
        ).order_by('pub_date')

    def get_context_data(self, **kwargs):
        context = super(ListView, self).get_context_data(**kwargs)
        current = Thread.objects.get(pk=self.kwargs.get('pk'))
        current.increase_view_count()
        context['thread'] = current
        context['title'] = context['thread'].title
        context['topic'] = context['thread'].topic
        context['form'] = ReplyForm()
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


def user_info(request, pk):
    u = User.objects.get(pk=pk)
    return render(request, 'forum/user_info.html', {
        'title': u.username,
        'user': u,
        'threads': u.threads.visible().select_related('topic')[:10],
        'replies': u.posts.visible().select_related('thread', 'user').order_by('-pub_date')[:30],
    })


class UserThreads(ListView):
    model = Post
    paginate_by = 15
    template_name = 'forum/user_threads.html'
    context_object_name = 'threads'

    def get_queryset(self):
        return Thread.objects.visible().filter(
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


class UserPosts(ListView):
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


class SearchView(ListView):
    model = Thread
    paginate_by = 20
    template_name = 'forum/search.html'
    context_object_name = 'threads'

    def get_queryset(self):
        keywords = self.kwargs.get('keyword')
        query = get_query(keywords, ['title'])
        return Thread.objects.visible().filter(
            query
        ).select_related(
            'user', 'topic'
        ).prefetch_related(
            'user__forum_avatar'
        ).order_by(
            get_thread_ordering(self.request)
        )

    def get_context_data(self, **kwargs):
        context = super(ListView, self).get_context_data(**kwargs)
        context['title'] = context['panel_title'] = _(
            'Search: ') + self.kwargs.get('keyword')
        context['show_order'] = True
        return context


def search_redirect(request):
    if request.method == 'GET':
        keyword = request.GET.get('keyword')
        return HttpResponseRedirect(reverse('forum:search', kwargs={'keyword': keyword}))
    else:
        return HttpResponseForbidden('Post you cannot')


@login_required
def create_thread(request, topic_pk=None, nodegroup_pk=None):
    topic = None
    node_group = NodeGroup.objects.all()
    fixed_nodegroup = NodeGroup.objects.filter(pk=nodegroup_pk)
    if topic_pk:
        topic = Topic.objects.get(pk=topic_pk)
    topics = Topic.objects.filter(node_group=nodegroup_pk)
    if request.method == 'POST':
        form = ThreadForm(request.POST, user=request.user)
        if form.is_valid():
            t = form.save()
            return HttpResponseRedirect(reverse('forum:thread', kwargs={'pk': t.pk}))
    else:
        form = ThreadForm()

    return render(request, 'forum/create_thread.html',
                  {'form': form, 'node_group': node_group, 'title': _('Create Thread'), 'topic': topic,
                   'fixed_nodegroup': fixed_nodegroup, 'topics': topics})


@login_required
def create_topic(request, nodegroup_pk=None):
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

    return render(request, 'forum/edit_thread.html', {'form': form, 'title': _('Edit thread')})


@login_required
def edit_post(request, pk):
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


class NotificationView(ListView):
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
    obj = Thread.objects.all()
    word_counter = {}
    for eachx in obj:
        words = TextBlob(eachx.title).noun_phrases
        for eachword in words:
            for singleword in eachword.split(" "):
                if singleword in word_counter:
                    print(singleword)
                    word_counter[singleword] += 1
                else:
                    word_counter[singleword] = 1

    popular_words = sorted(word_counter, key=word_counter.get, reverse=True)
    return popular_words[:number_of_keyword]
