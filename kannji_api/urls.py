from django.conf.urls import url, include

from kannji_api import index


urlpatterns = [
    url(r'^$', index.index, name='index'),
    # url(r'^v(?P<version>[1-9][0-9]*)/$', include('kannji_api.v2.urls')),
    url(r'^v1/', include('kannji_api.v1.urls')),
    url(r'^v2/', include('kannji_api.v2.urls')),
    url(r'^v3/', include('kannji_api.v3.urls')),
]
