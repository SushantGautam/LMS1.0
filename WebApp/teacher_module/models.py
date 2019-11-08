from WebApp.models import MemberInfo

USER_MODEL = MemberInfo

# class Post(models.Model):
#     thread = models.ForeignKey('thread', related_name='replies', verbose_name=("thread"),on_delete=models.CASCADE)
#     user = models.ForeignKey(USER_MODEL, related_name='posts', verbose_name=("user"),on_delete=models.CASCADE)
#     content_raw = models.TextField(verbose_name=("raw content"))
#     content_rendered = models.TextField(default='', verbose_name=("rendered content"))
#     pub_date = models.DateTimeField(auto_now_add=True, verbose_name=("published time"))
#     hidden = models.BooleanField(default=False, verbose_name=("hidden"))
#     objects = PostQueryset.as_manager()

#     raw_content_hash = None

#     def __init__(self, *args, **kwargs):
#         super(Post, self).__init__(*args, **kwargs)
#         self.raw_content_hash = xxhash.xxh64(self.content_raw).hexdigest()

#     def __str__(self):
#         return 'Reply to %s' % self.thread.title

#     def save(self, *args, **kwargs):
#         new_hash = xxhash.xxh64(self.content_raw).hexdigest()
#         mentioned_users = []
#         if new_hash != self.raw_content_hash or (not self.pk):
#             self.content_rendered, mentioned_users = render_content(self.content_raw, sender=self.user.username)
#         super(Post, self).save(*args, **kwargs)
#         t = self.thread
#         t.reply_count = t.get_reply_count()
#         t.last_replied = t.get_last_replied()
#         t.save(update_fields=['last_replied', 'reply_count'])
#         for to in mentioned_users:
#             notify(to=to.username, sender=self.user.username, post=self.pk)

#     def delete(self, *args, **kwargs):
#         super(Post, self).delete(*args, **kwargs)
#         t = self.thread
#         t.reply_count = t.get_reply_count()
#         t.last_replied = t.get_last_replied()
#         t.save(update_fields=['last_replied', 'reply_count'])
