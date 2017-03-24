from django.http import HttpResponse

from kannji_api.kanji_model import Kanji
from kannji_api.list_model import LearningLists, LearningListEntries


def createJlptLists(response):

    # createJlptListByNiveau(3)
    # createJlptListByNiveau(2)
    # createJlptListByNiveau(1)

    return HttpResponse("yay")


def createJlptListByNiveau(niveau):
    jlptKanji = Kanji.objects.filter(jlpt_level=niveau)

    jlptList = LearningLists(name="JLPT N" + str(niveau) + " english")

    jlptList.save()

    for kanji in jlptKanji:
        entry = LearningListEntries(list_id=jlptList.list_id, kanji_id=kanji.kanji_id)
        entry.save()
        jlptList.listentries_set.add(entry)
