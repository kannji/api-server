from django.http import HttpResponse

from kannji_api.models import Kanji, LearningLists


def create_jlpt_lists(response):
	create_jlpt_list_by_niveau(4)
	create_jlpt_list_by_niveau(3)
	create_jlpt_list_by_niveau(2)
	create_jlpt_list_by_niveau(1)
	
	return HttpResponse("yay")


def create_jlpt_list_by_niveau(niveau):
	jlpt_kanji = Kanji.objects.filter(jlpt_level=niveau)
	
	jlpt_list = LearningLists(name="JLPT N" + str(niveau) + " english")
	
	jlpt_list.save()
	
	for kanji in jlpt_kanji:
		jlpt_list.kanji.add(kanji)
