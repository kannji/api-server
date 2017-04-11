from django.http import HttpResponse

from kannji_api.models import Kanji, LearningLists


def createJlptLists(response):
	createJlptListByNiveau(4)
	createJlptListByNiveau(3)
	createJlptListByNiveau(2)
	createJlptListByNiveau(1)
	
	return HttpResponse("yay")


def createJlptListByNiveau(niveau):
	jlptKanji = Kanji.objects.filter(jlpt_level=niveau)
	
	jlptList = LearningLists(name="JLPT N" + str(niveau) + " english")
	
	jlptList.save()
	
	for kanji in jlptKanji:
		jlptList.kanji.add(kanji)
