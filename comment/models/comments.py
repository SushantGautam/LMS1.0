from django.contrib.auth import get_user_model
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models

from comment.managers import CommentManager


class Comment(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, default=None)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    content = models.TextField()
    urlhash = models.CharField(
        max_length=50,
        unique=True,
        editable=False
    )
    posted = models.DateTimeField(auto_now_add=True)
    edited = models.DateTimeField(auto_now=True)

    is_visible = models.BooleanField(default=True)
    is_closed = models.BooleanField(default=False)

    objects = CommentManager()

    class Meta:
        ordering = ['-posted', ]

    def __str__(self):
        if not self.parent:
            return f'comment by {self.user}: {self.content[:20]}'
        else:
            return f'reply by {self.user}: {self.content[:20]}'

    def __repr__(self):
        return self.__str__()

    def _get_reaction_count(self, reaction_type):
        return getattr(self.reaction, reaction_type, None)

    def replies(self, include_flagged=False):
        if include_flagged:
            return self.__class__.objects.filter(parent=self).order_by('posted')
        return self.__class__.objects.all_exclude_flagged().filter(parent=self).order_by('posted')

    def _set_unique_urlhash(self):
        if not self.urlhash:
            self.urlhash = self.__class__.objects.generate_urlhash()
            while self.__class__.objects.filter(urlhash=self.urlhash).exists():
                self.urlhash = self.__class__.objects.generate_urlhash()

    def save(self, *args, **kwargs):
        self._set_unique_urlhash()
        super(Comment, self).save(*args, **kwargs)

    @property
    def is_parent(self):
        return self.parent is None

    @property
    def is_edited(self):
        return self.posted.timestamp() + 1 < self.edited.timestamp()

    @property
    def likes(self):
        return self._get_reaction_count('likes')

    @property
    def dislikes(self):
        return self._get_reaction_count('dislikes')

    @property
    def is_flagged(self):
        if hasattr(self, 'flag') and self.flag.is_flag_enabled:
            return self.flag.state != self.flag.UNFLAGGED
        return False

    @property
    def has_flagged_state(self):
        if hasattr(self, 'flag'):
            return self.flag.state == self.flag.FLAGGED
        return False

    @property
    def has_rejected_state(self):
        if hasattr(self, 'flag'):
            return self.flag.state == self.flag.REJECTED
        return False

    @property
    def has_resolved_state(self):
        if hasattr(self, 'flag'):
            return self.flag.state == self.flag.RESOLVED
        return False