from django.conf.urls import url

from kannji_api.v2 import index as index_v2, lists as list_v2

urlpatterns = [
	# changed part of the api
	url(r'^$', index_v2.index, name='index'),
	url(r'^lists/all/$', list_v2.get_all_learning_lists_brief, name='get_all_learning_lists_brief'),
	url(r'^lists/(?P<learning_list_id>[0-9]+)/$', list_v2.get_learning_list_detail, name='get_learning_list_detail'),
	url(r'^lists/(?P<learning_list_id>[0-9]+)/random$', list_v2.get_random_learning_entry_from_learning_list,
	    name='get_random_learning_entry_from_learning_list'),
]
