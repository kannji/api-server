from django.conf.urls import url, include
import oauth2_provider.views as oauth2_views

from kannji_api.v3 import index as index_v3, user as user_v3

urlpatterns = [
    # changed part of the api
    url(r'^oauth2/token/$', oauth2_views.TokenView.as_view(), name="token"),
    url(r'^oauth2/revoke-token/$', oauth2_views.RevokeTokenView.as_view(), name="revoke-token"),
    url(r'^$', index_v3.index, name='index'),
    url(r'^user/$', user_v3.user_profile, name='index'),

    # unchanged part
    url(r'^', include('kannji_api.v2.urls')),
]