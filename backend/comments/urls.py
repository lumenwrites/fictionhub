from django.conf.urls import url

from .views import comment_submit, reply_submit
from .views import comment_edit, comment_delete
from .views import comment_upvote, comment_unupvote

urlpatterns = [
    # Comments
    url(r'^comment-submit/(?P<post_slug>[^\.]+)', comment_submit),
    url(r'^reply/(?P<post_slug>[^\.]+)/(?P<comment_id>[^\.]+)/', reply_submit),

    url(r'^comment/(?P<post_slug>[^\.]+)/(?P<comment_id>[^\.]+)/edit', comment_edit),
    url(r'^comment/(?P<post_slug>[^\.]+)/(?P<comment_id>[^\.]+)/delete', comment_delete),

    url(r'^comment-upvote/', comment_upvote),
    url(r'^comment-unupvote/', comment_unupvote),
]
