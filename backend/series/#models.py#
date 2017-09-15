from django.db import models

class Series(models.Model):
    title = models.CharField(max_length=256, null=True, blank=True)
    slug = models.SlugField(max_length=256, default="", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    free_chapters = models.IntegerField(default=4)
    price = models.FloatField(default=0)    
    
    class Meta:
        verbose_name_plural = "series"

    def __str__(self):
        if self.title:
            return self.title[:100]
        else:
            return "Series"
