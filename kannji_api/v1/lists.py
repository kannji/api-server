from django.http import JsonResponse
from django.shortcuts import get_object_or_404

from kannji_api.list_model import LearningLists
from kannji_api.v1.kanji import get_kanji_object


def get_list(response, list_id):
	# get list
	learning_list = get_object_or_404(LearningLists, list_id=list_id)
	
	return JsonResponse(get_learning_list_object(learning_list))


def get_all_lists_brief(response):
	# get list
	learning_lists = LearningLists.objects.all()
	
	learning_lists_object = {}
	
	for learning_list in learning_lists:
		learning_lists_object[learning_list.list_id] = get_learning_list_brief_object(learning_list)
	
	return JsonResponse(learning_lists_object)


def get_learning_list_brief_object(learning_list):
	learningListBriefObject = {}
	learningListBriefObject['list_id'] = learning_list.list_id
	learningListBriefObject['name'] = learning_list.name
	learningListBriefObject['description'] = learning_list.description
	learningListBriefObject['thumbnail_url'] = learning_list.thumbnail_url
	
	return learningListBriefObject


def get_learning_list_object(learning_list):
	learningListObject = get_learning_list_brief_object(learning_list)
	learningListObject['entries'] = {}
	
	# add kanji to the list
	kanji = learning_list.kanji.all()
	
	for current_kanji in kanji:
		kanjiObject = get_kanji_object(current_kanji)
		kanjiObject['type'] = 'kanji'
		learningListObject['entries'][current_kanji.kanji_id] = kanjiObject
	
	return learningListObject
