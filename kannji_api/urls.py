from django.conf.urls import url

from . import kanji

urlpatterns = [
    url(r'^$', kanji.index, name='index'),
    url(r'^kanji/$', kanji.get_all_kanji, name='get_all_kanji'),
    url(r'^kanji/(?P<kanji_id>[0-9]+)/$', kanji.get_kanji, name='get_kanji'),
    url(r'^kanji/random/$', kanji.get_random_kanji, name='get_random_kanji'),
]
