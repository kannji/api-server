import time
from django.http import HttpResponse, JsonResponse
from lxml import etree
from kannji_api.kanji_model import Kanji, KanjiReadings, KanjiMeanings, KanjiRadicals
from parser.parsing_helper import xpathGetInt, xpathGetStr


def update(request):
    # some statistics
    startTime = time.time()
    updateCount = 0
    updateList = []
    addCount = 0
    addedList = []
    skipCount = 0
    skipList = []

    i = 0
    for event, word in etree.iterparse("jmdict_parser/JMdict.xml", tag="entry"):
        i += 1
        if i > 10:
            break

        wordID = xpathGetInt(word, "ent_seq")

        literal = xpathGetStr(word, "k_ele[not(ke_inf/text()='&oK;')]/keb")

        frequency = xpathGetStr(word, "k_ele[not(ke_inf/text()='&oK;')]/ke_pri")

        reading = xpathGetStr(word, "r_ele/reb")

        addedList.append(wordID)
        addedList.append(frequency)
        addedList.append(literal)
        addedList.append(reading)

    return JsonResponse(addedList, safe=False)
