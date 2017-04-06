from django.conf.urls import url, include
from django.http import HttpResponse

from kannji_api.v3 import index as index_v3

urlpatterns = [
    # changed part of the api
    url(r'^oauth2/', include('oauth2_provider.urls', namespace='oauth2_provider')),
    url(r'^$', index_v3.index, name='index'),
    url(r'^secret/$', index_v3.secret_page, name='index'),

    # unchanged part
    url(r'^', include('kannji_api.v2.urls')),
]