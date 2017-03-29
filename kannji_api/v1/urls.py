from django.conf.urls import url

from kannji_api.v1 import index, lists, kanji

urlpatterns = [
    url(r'^$', index.index, name='index'),
    url(r'^lists/(?P<list_id>[0-9]+)/$', lists.get_list, name='get_list'),
    url(r'^lists/all/$', lists.get_all_lists_brief, name='get_all_lists_brief'),
    url(r'^kanji/$', kanji.get_all_kanji, name='get_all_kanji'),
    url(r'^kanji/(?P<kanji_id>[0-9]+)/$', kanji.get_kanji, name='get_kanji'),
    url(r'^kanji/random/$', kanji.get_random_kanji, name='get_random_kanji'),
]
