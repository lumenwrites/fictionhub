from django.conf.urls import url

from .views import series_update, series_purchase,purchase

urlpatterns = [
    url(r'^series/(?P<slug>[^\.]+)/update$', series_update),    
    url(r'^series/(?P<slug>[^\.]+)/(?P<username>[^\.]+)/purchase$', series_purchase),
    url(r'^purchase$', purchase),    
]
