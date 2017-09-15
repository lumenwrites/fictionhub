from django.conf.urls import url

from .views import inbox

urlpatterns = [
    url(r'^inbox/$', inbox),
]
