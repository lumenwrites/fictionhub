from datetime import datetime
import uuid # for unique slug
from markdown import Markdown   # To parse meta data
from django.db import models
from django.template.defaultfilters import slugify
from django.conf import settings
from django.db.models import permalink

from tags.models import Tag
from categories.models import Category
from series.models import Series



# Generate unique slug
def unique_slug(title):
    uniqueid = uuid.uuid1().hex[:5]                
    slug = slugify(title) + "-" + str(uniqueid)

    if not Post.objects.filter(slug=slug).exists():
        # If there's no posts with such slug,
        # then the slug is unique, so I return it
        return slug
    else:
        # If the post with this slug already exists -
        # I try to generate unique slug again
        return unique_slug(title)

    
class Post(models.Model):
    slug = models.SlugField(max_length=256, default="")    
    body = models.TextField(default="", null=True, blank=True)

    published = models.BooleanField(default=False, blank=True)
    created_at = models.DateTimeField(blank=True, null=True)
    published_at = models.DateTimeField(blank=True, null=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL,
                               on_delete=models.CASCADE,
                               related_name="posts",
                               null=True)    
    
    tags = models.ManyToManyField('tags.Tag',
                                  related_name="posts",
                                  blank=True)
    category = models.ForeignKey('categories.Category',
                                 on_delete=models.CASCADE,
                                 related_name="posts",
                                  blank=True, null=True)    

    score = models.IntegerField(default=0)
    views = models.IntegerField(default=0)

    # Chapter
    series = models.ForeignKey('series.Series', related_name="chapters",
                               default=None, null=True, blank=True, on_delete=models.CASCADE)
    # chapter_number = models.IntegerField(default=1) 


    def __str__(self):
        return self.body[:100]

    def save(self, slug="", *args, **kwargs):
        if not self.id:
            self.created_at = datetime.now()
            
            # Parsing meta data (if it's there, for a Screenplay)
            md = Markdown(extensions = ['markdown.extensions.meta'])
            html = md.convert(self.body)    
            if "title" in md.Meta:
                # If it's a screenplay
                title = md.Meta["title"]
                self.slug = unique_slug(title)                
            else:
                # Turn header or the first line into a slug
                firstline = self.body.splitlines()[0]
                self.slug = unique_slug(firstline[:30])

        return super(Post, self).save(*args, **kwargs)
    
    @permalink
    def get_absolute_url(self):
        return ('post-detail', None, {'slug': self.slug })

    class Meta:
        ordering = ['created_at']
