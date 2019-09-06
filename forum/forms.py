# -*- coding: utf-8 -*-
from django.forms import ModelForm
from django.conf import settings
from crispy_forms.layout import Submit
from crispy_forms.helper import FormHelper
from .models import Thread, Appendix, ForumAvatar, Post, Topic
from django.utils.translation import ugettext as _

if 'pagedown' in settings.INSTALLED_APPS:
    use_pagedown = True
    from django import forms
    from pagedown.widgets import PagedownWidget
else:
    use_pagedown = False


class ThreadForm(ModelForm):

    if use_pagedown:
        content_raw = forms.CharField(label=_('Content'), widget=PagedownWidget())

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(ThreadForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.add_input(Submit('submit', _('Submit')))

    class Meta:
        model = Thread
        fields = ['topic', 'title', 'content_raw']
        labels = {
            'content_raw': _('Content'),
            'topic': _('Topic'),
            'title': _('Title'),
        }

    def save(self, commit=True):
        inst = super(ThreadForm, self).save(commit=False)
        inst.user = self.user
        if commit:
            inst.save()
            self.save_m2m()
        return inst


class ThreadEditForm(ModelForm):

    if use_pagedown:
        content_raw = forms.CharField(label=_('Content'), widget=PagedownWidget())

    def __init__(self, *args, **kwargs):
        super(ThreadEditForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.add_input(Submit('submit', _('Submit')))

    class Meta:
        model = Thread
        fields = ('content_raw', )
        labels = {
            'content_raw': _('Content'),
        }
class TopicForm(ModelForm):

    if use_pagedown:
        content_raw = forms.CharField(label=_('Content'), widget=PagedownWidget())

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(TopicForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.add_input(Submit('submit', _('Submit')))

    class Meta:
        model = Topic
        fields = ['node_group','title','description','topic_icon' ]
        labels = {
            'node_group':_('NodeGroup'),
            'description': _('Description'),
            'title': _('Title'),
            'topic_icon': _('Topic Icon'),
        }

    def save(self, commit=True):
        inst = super(TopicForm, self).save(commit=False)
        inst.user = self.user
        if commit:
            inst.save()
            self.save_m2m()
        return inst


class TopicEditForm(ModelForm):

    if use_pagedown:
        content_raw = forms.CharField(label=_('Content'), widget=PagedownWidget())

    def __init__(self, *args, **kwargs):
        super(TopicEditForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.add_input(Submit('submit', _('Submit')))

    class Meta:
        model = Topic
        fields = ('description','topic_icon', )
        labels = {
            'description': _('Description'),
            'topic_icon': _('Topic Icon'),
        }


class AppendixForm(ModelForm):

    def __init__(self, *args, **kwargs):
        self.thread = kwargs.pop('thread', None)
        super(AppendixForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.add_input(Submit('submit', _('Submit')))

    class Meta:
        model = Appendix
        fields = ('content_raw', )
        labels = {
            'content_raw': _('Content'),
        }

    def save(self, commit=True):
        inst = super(AppendixForm, self).save(commit=False)
        inst.thread = self.thread
        if commit:
            inst.save()
            self.save_m2m()
        return inst


class ForumAvatarForm(ModelForm):

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(ForumAvatarForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.add_input(Submit('submit', _('Submit')))

    class Meta:
        model = ForumAvatar
        fields = ('image', 'use_gravatar')
        labels = {
            'image': _('Avatar Image'),
            'use_gravatar': _("Always Use Gravatar")
        }

    def save(self, commit=True):
        inst = super(ForumAvatarForm, self).save(commit=False)
        inst.user = self.user
        if commit:
            inst.save()
            self.save_m2m()
        return inst


class ReplyForm(ModelForm):

    if use_pagedown:
        content_raw = forms.CharField(label='', widget=PagedownWidget())

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        self.thread_id = kwargs.pop('thread_id', None)
        super(ReplyForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.add_input(Submit('submit', _('Submit')))

    class Meta:
        model = Post
        fields = ('content_raw',)
        labels = {
            'content_raw': '',
        }

    def save(self, commit=True):
        inst = super(ReplyForm, self).save(commit=False)
        inst.user = self.user
        inst.thread_id = self.thread_id
        if commit:
            inst.save()
            self.save_m2m()
        return inst


class PostEditForm(ModelForm):

    if use_pagedown:
        content_raw = forms.CharField(label=_('Content'), widget=PagedownWidget())

    def __init__(self, *args, **kwargs):
        super(PostEditForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.add_input(Submit('submit', _('Submit')))

    class Meta:
        model = Post
        fields = ('content_raw', )
        labels = {
            'content_raw': _('Content'),
        }