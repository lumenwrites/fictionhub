from django.conf.urls import url
from django.contrib.auth.views import logout

from .views import login, join, email_subscribe
from .views import settings, update_password
from .views import subscribe, unsubscribe
from .views import leaderboard

urlpatterns = [
    url(r'^join/', join),
    url('^login/$', login),
    url(r'^logout/', logout),

    url(r'^@(?P<username>[^\.]+)/subscribe', subscribe),
    url(r'^@(?P<username>[^\.]+)/unsubscribe', unsubscribe),
    
    url(r'^settings/$', settings),
    url(r'^update-password/$', update_password),

    url(r'^subscribe/', email_subscribe),

    # Top Users
    url(r'^leaderboard/$', leaderboard),
    
    
]
