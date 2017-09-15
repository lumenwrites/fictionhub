from django.db import models

# Create your models here.

class Source(models.Model):
    url = models.URLField(default="", null=True, blank=True)

    def __str__(self):
        return self.url
    
