"""backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/dev/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static


from posts import urls as posts_urls
from profiles import urls as profiles_urls
from notifications import urls as notifications_urls
from comments import urls as comments_urls
from series import urls as series_urls

from . import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),

    url(r'^$', views.home),
    url(r'^home/$', views.home),        
    url(r'^about$', views.about),
    url(r'^newsletter$', views.newsletter),
    
    url(r'', include(comments_urls)),            
    url(r'', include(profiles_urls)),
    url(r'', include(notifications_urls)),
    url(r'', include(series_urls)),
    url(r'', include(posts_urls)),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
