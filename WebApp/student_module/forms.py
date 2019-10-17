
import datetime

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django import forms
from django.conf import settings
from django.forms import ModelForm
from django.forms import SelectDateWidget
from django.utils.translation import ugettext as _
from forum.models import Thread, ForumAvatar, Post, Topic
from forum.forms import TopicForm


if 'pagedown' in settings.INSTALLED_APPS:
    use_pagedown = True
    from django import forms
    from pagedown.widgets import PagedownWidget
else:
    use_pagedown = False


class ThreadForm(ModelForm):
    if use_pagedown:
        content_raw = forms.CharField(
            label=_('Content'), widget=PagedownWidget())

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(ThreadForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.add_input(Submit('submit', ('Submit')))

    class Meta:
        model = Thread
        fields = ['topic', 'title', 'content_raw']
        labels = {
            'content_raw': ('Content'),
            'topic': ('Topic'),
            'title': ('Title'),
        }

    def save(self, commit=True):
        inst = super(ThreadForm, self).save(commit=False)
        inst.user = self.user
        if commit:
            inst.save()
            self.save_m2m()
        return inst


class TopicForm(TopicForm):


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
