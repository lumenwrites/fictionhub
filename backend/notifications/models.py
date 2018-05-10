from datetime import datetime

from django.db import models
from django.conf import settings


class Message(models.Model):
    from_user = models.ForeignKey(settings.AUTH_USER_MODEL,
                                  related_name="sent_messages", default="", on_delete=models.CASCADE)
    to_user = models.ForeignKey(settings.AUTH_USER_MODEL,
                                related_name="received_messages", default="", on_delete=models.CASCADE) 
    body = models.TextField(default="", null=True, blank=True)

    created_at = models.DateTimeField(blank=True, null=True)
    isread = models.BooleanField(default=False)
    email_sent = models.BooleanField(default=False)

    # Parent for replies?

    def __str__(self):
        return self.body[:100] \
            + " from " + str(self.from_user) \
            + " to " + str(self.to_user)

    def save(self, *args, **kwargs):
        if not self.id:
            self.created_at = datetime.now()

        return super(Message, self).save(*args, **kwargs)
