from markdown import Markdown

from django.contrib.syndication.views import Feed
from django.utils.feedgenerator import Atom1Feed
from django.shortcuts import get_object_or_404

from .models import Post
from profiles.models import User


# All posts
# Series feed


class UserFeed(Feed):
    title = "fictionhub latests stories"
    link = "/"
    feed_type = Atom1Feed

    def get_object(self, request, username):
        return get_object_or_404(User, username=username)

    def title(self, obj):
        return "%s latest stories" % obj.username

    def link(self, obj):
        return "http://fictionhub.io/@" + obj.username
        # return "http://fictionhub.io/" +  str(item.get_absolute_url())
    
    def items(self, obj):
        return Post.objects.filter(published=True, author=obj).order_by("-published_at")

    def item_title(self, item):
        firstline = item.body.splitlines()[0]
        md = Markdown()
        return md.convert(firstline)

    def item_link(self, item):
        return "http://fictionhub.io" + item.get_absolute_url()
    
    def item_pubdate(self, item):
        return item.published_at

    def item_description(self, item):
        md = Markdown()
        return md.convert(item.body)



