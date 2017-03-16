from django.conf.urls import url

from jlpt_list_creator import jlpt_list_creator
from kannji_api import lists
from kannji_api import kanji

urlpatterns = [
    url(r'^$', kanji.index, name='index'),
    url(r'^lists/$', kanji.index, name='index'),
    url(r'^lists/(?P<list_id>[0-9]+)/$', lists.get_list, name='index'),
    url(r'^lists/all/$', lists.get_all_lists_brief, name='index'),
    url(r'^kanji/$', kanji.get_all_kanji, name='get_all_kanji'),
    url(r'^kanji/(?P<kanji_id>[0-9]+)/$', kanji.get_kanji, name='get_kanji'),
    url(r'^kanji/random/$', kanji.get_random_kanji, name='get_random_kanji'),
]
