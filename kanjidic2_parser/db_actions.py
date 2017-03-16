import time
from parser.parsing_helper import xpathGetInt, xpathGetStr
from django.http import HttpResponse, JsonResponse
from lxml import etree
from kannji_api.kanji_model import Kanji, KanjiReadings, KanjiMeanings, KanjiRadicals
from django.db import connection,transaction


def clearDatabase(request):
    Kanji.objects.all().delete()
    KanjiMeanings.objects.all().delete()
    KanjiReadings.objects.all().delete()
    KanjiRadicals.objects.all().delete()

    with connection.cursor() as cursor:
        cursor.execute("ALTER TABLE `kanji` AUTO_INCREMENT = 1;")
        cursor.execute("ALTER TABLE `kanji_meanings` AUTO_INCREMENT = 1;")
        cursor.execute("ALTER TABLE `kanji_readings` AUTO_INCREMENT = 1;")
        cursor.execute("ALTER TABLE `kanji_radicals` AUTO_INCREMENT = 1;")


def rebuildDatabase(request):
    clearDatabase(request)
    return updateDatabase(request)


def addKanjiFromXml(literal, character):
    # get all kanji info
    stroke_count = xpathGetInt(character, "misc/stroke_count")
    jlptLevel = xpathGetInt(character, "misc/jlpt")
    schoolGrade = xpathGetInt(character, "misc/grade")
    frequency = xpathGetInt(character, "misc/freq")

    # add the kanji to the db
    kanji = Kanji(
        literal=literal,
        stroke_count=stroke_count,
        jlpt_level=jlptLevel,
        school_grade=schoolGrade,
        frequency=frequency
    )
    kanji.save()

    if Kanji.objects.filter(literal=literal).exists():
        # add foreign info
        # radicals
        for radical in character.xpath("radical/rad_value"):
            KanjiRadicals(kanji_id=kanji, radical=radical.text, type=radical.attrib.get("rad_type")).save()

        # readings
        # on
        for reading in character.xpath("reading_meaning/rmgroup/reading[@r_type='ja_on']/text()"):
            KanjiReadings(kanji_id=kanji, reading=reading, type="onyomi").save()

        # kun
        for reading in character.xpath("reading_meaning/rmgroup/reading[@r_type='ja_kun']/text()"):
            KanjiReadings(kanji_id=kanji, reading=reading, type="kunyomi").save()

        # nanori
        for reading in character.xpath("reading_meaning/nanori/text()"):
            KanjiReadings(kanji_id=kanji, reading=reading, type="nanori").save()

        # meanings
        for meaning in character.xpath("reading_meaning/rmgroup/meaning[not(@m_lang)]/text()"):
            KanjiMeanings(kanji_id=kanji, meaning=meaning, language="en-GB").save()

        return True
    else:
        # adding kanji didn't work, so we delete it. (fuck you encoding)
        kanji.delete()
        return False


def updateKanjiFromXml(literal, character):
    pass


def updateDatabase(request):
    # some statistics
    startTime = time.time()
    updateCount = 0
    updateList = []
    addCount = 0
    addedList = []
    skipCount = 0
    skipList = []

    # looping through all characters (kanji) in xml file
    #i = 0
    for event, character in etree.iterparse("kanjidic2_parser/kanjidic2.xml", tag="character"):
        #i += 1
        #if i > 10:
        #    break

        # get literal and have a look what to do with it
        literal = xpathGetStr(character, "literal")

        # try getting the kanji from db
        if Kanji.objects.filter(literal=literal).exists():
            updateKanjiFromXml(literal, character)
            updateCount += 1
            updateList.append(literal)
        else:
            kanjiAdded = addKanjiFromXml(literal, character)
            if kanjiAdded:
                addCount += 1
                addedList.append(literal)
            else:
                skipCount += 1
                skipList.append(literal)

        # clear the character to save ram
        character.clear()

    # some statistics
    endTime = time.time()

    return HttpResponse(
        'updated:' + str(updateCount) + '<br>\n' +
        'added:' + str(addCount) + '<br>\n' +
        'skipped:' + str(skipCount) + '<br>\n' +
        'Time needed: ' + str(endTime-startTime) + '<br><br>\n' +
        'updated kanji: <br>\n' +
        ', '.join(updateList) + '<br><br>\n' +
        'addded kanji: <br>\n' +
        ', '.join(addedList) + '<br><br>\n' +
        'skipped kanji: <br>\n' +
        ', '.join(skipList) + '<br><br>\n'
    )
