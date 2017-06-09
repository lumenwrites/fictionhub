import datetime

from django.db import models
from django.template.defaultfilters import slugify
from django.conf import settings
from django.db.models import permalink

from posts.models import Post

class Comment(models.Model):
    post = models.ForeignKey('posts.Post',
                             on_delete=models.CASCADE,
                             related_name="comments",
                             default=None, null=True, blank=True)    
    parent = models.ForeignKey('Comment',
                               on_delete=models.CASCADE,
                               related_name="children",
                               default=None, null=True, blank=True)
    body = models.TextField()    
    author = models.ForeignKey(settings.AUTH_USER_MODEL,
                               on_delete=models.CASCADE,
                               related_name="comments", default="")
    score = models.IntegerField(default=0)
    created_at = models.DateTimeField(blank=True, null=True)


    def __str__(self):
        string_name = ""
        try:
            string_name = self.body
        except:
            string_name = "comment"
        if len(string_name) > 64:
            string_name = string_name[:64] + "..."
        return string_name
    

    @permalink
    def get_absolute_url(self):
        return ('comment-permalink', None, {'comment_id': self.id })

    def save(self, *args, **kwargs):
        if not self.id:
            self.created_at = datetime.datetime.now()
        return super(Comment, self).save(*args, **kwargs)    
