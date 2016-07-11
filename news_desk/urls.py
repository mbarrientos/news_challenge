"""news_desk URL Configuration
"""
from django.conf.urls import url, include
from django.contrib import admin


urlpatterns = [
    url(r'^news/', include('news.urls')),
    url(r'^admin/', admin.site.urls),
]
