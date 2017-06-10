from django.db import models

class Series(models.Model):
    title = models.CharField(max_length=256, null=True, blank=True)
    slug = models.SlugField(max_length=256, default="", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "series"

    def __str__(self):
        return self.title[:100]

