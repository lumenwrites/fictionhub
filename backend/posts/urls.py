from django.conf.urls import url

from .views import BrowseView, ProfileView, SubscriptionsView
from .views import PostDetailView, post_create, post_edit, post_delete
from .views import upvote, unupvote, post_publish, post_unpublish
from .feeds import UserFeed

urlpatterns = [

    url(r'^@(?P<username>[^\.]+)/posts.atom$', UserFeed()),        

    url(r'^@(?P<username>[^\.]+)/tag/(?P<tag>[^\.]+)/$', ProfileView.as_view()),        
    url(r'^@(?P<username>[^\.]+)/(?P<category>[^\.]+)/$', ProfileView.as_view()),
    url(r'^@(?P<username>[^\.]+)/$', ProfileView.as_view()),
    url(r'^post/(?P<slug>[^\.]+)/edit$', post_edit),    
    url(r'^post/(?P<slug>[^\.]+)/delete$', post_delete),
    url(r'^post/(?P<slug>[^\.]+)/publish$', post_publish),
    url(r'^post/(?P<slug>[^\.]+)/unpublish$', post_unpublish),        
    url(r'^post/(?P<slug>[^\.]+)/$', PostDetailView.as_view(), name='post-detail'),
    url(r'^story/(?P<slug>[^\.]+)/$', PostDetailView.as_view()),    

    url(r'^create$', post_create),    
    url(r'^write$', post_create),

    url(r'^upvote/$', upvote),
    url(r'^unupvote/$', unupvote),

    url(r'^browse/$', BrowseView.as_view()),    
    url(r'^subscriptions/$', SubscriptionsView.as_view()),    
    url(r'^tag/(?P<tag>[^\.]+)/$', BrowseView.as_view()),
    url(r'^(?P<category>[^\.]+)/$', BrowseView.as_view()),
    url(r'^$', BrowseView.as_view()),
]
