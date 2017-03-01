from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^kanji/$', views.get_all_kanji, name='get_all_kanji'),
    url(r'^kanji/(?P<kanji_id>[0-9]+)/$', views.get_kanji, name='get_kanji'),
]
