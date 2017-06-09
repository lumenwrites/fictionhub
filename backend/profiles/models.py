from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models import permalink

from posts.models import Post
from notifications.models import Message
from comments.models import Comment

class User(AbstractUser):  
    karma = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    upvoted = models.ManyToManyField('posts.Post', related_name="upvoters", blank=True)
    comments_upvoted = models.ManyToManyField('comments.Comment', related_name="upvoters", blank=True)    

    subscribed_to = models.ManyToManyField('User',
                                           related_name="subscribers",
                                           blank=True)
    # About
    about = models.TextField(max_length=512, blank=True)
    website = models.CharField(max_length=64, blank=True)

    # Email notifications
    # email_subscriptions = models.BooleanField(default=True,
    # verbose_name='Send me email notifications when someone I follow publishes a new story')
    # email_comments = models.BooleanField(default=True,
    # verbose_name='Send me email notifications when someone replies to my story or comment')

    @permalink
    def get_absolute_url(self):
        return ('user_profile', None, {'username': self.username })        

    def has_unread_notifications(self):
        if Message.objects.filter(to_user=self, isread=False):
            return True
        else:
            return False            
    

# Email subscriber
class Subscriber(models.Model):
    email = models.CharField(max_length=64, blank=True, null=True)
    ref = models.CharField(max_length=64, blank=True, default="", null=True)        

    def __str__(self):
        if not self.ref:
            return self.email
        else:
            return self.ref + " | " + self.email
