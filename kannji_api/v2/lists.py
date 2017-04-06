from django.http import JsonResponse
from django.shortcuts import get_object_or_404

from kannji_api.list_model import LearningLists
from kannji_api.v1.kanji import get_kanji_object
from kannji_api.v1.lists import get_learning_list_brief_object
from kannji_api.v2.pagination_helper import get_paginator, get_page_index_from_request


def get_all_learning_lists_brief(request):
	# get the paginator
	learning_lists = LearningLists.objects.all()
	paginator = get_paginator(learning_lists, request)
	
	# get the current page
	page_index = get_page_index_from_request(request)
	
	# add all learning lists as objects on current page to array
	learning_lists_response = []
	
	for learning_list in paginator.page(page_index):
		learning_lists_response.append(get_learning_list_brief_object(learning_list))
	
	# put together the response
	response = {
		'page_count': paginator.num_pages,
		'learning_lists': learning_lists_response
	}
	
	return JsonResponse(response)


def get_learning_list_detail(request, learning_list_id):
	# get the learning-list
	learning_list = get_object_or_404(LearningLists, list_id=learning_list_id)
	
	# get entries paginated
	# get the paginator
	learning_list_kanji = learning_list.kanji.all()
	paginator = get_paginator(learning_list_kanji, request)
	
	# get the current page
	page_index = get_page_index_from_request(request)
	
	# add all learning lists as objects on current page to array
	learning_list_kanji_response = []
	
	for current_kanji in paginator.page(page_index):
		kanji_object = get_kanji_object(current_kanji)
		kanji_object['type'] = 'kanji'
		learning_list_kanji_response.append(kanji_object)
	
	# put together the response
	# get the brief information about the list
	learning_list_response = get_learning_list_brief_object(learning_list)
	learning_list_response['learning_entries_page'] = {
		'page_count': paginator.num_pages,
		'learning_entries': learning_list_kanji_response
	}
	
	return JsonResponse(learning_list_response)


def get_random_learning_entry_from_learning_list(request, learning_list_id):
	# TODO listen to filter set in request
	learning_list = get_object_or_404(LearningLists, list_id=learning_list_id)
	kanji = learning_list.kanji.order_by('?').first()
	return JsonResponse(get_kanji_object(kanji))
