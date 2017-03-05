from django.http import HttpResponse, JsonResponse
from lxml import etree
from kannji_api.models import Kanji, KanjiReadings, KanjiMeanings, KanjiRadicals


def update(request):
    kanjidic2File = open("kanjidic2_parser/kanjidic2.xml", "rb", buffering=0)

    root = etree.fromstring(kanjidic2File.read())

    characters = root.xpath("character")
    # characters = characters[0:10]

    Kanji.objects.all().delete()
    KanjiReadings.objects.all().delete()
    KanjiMeanings.objects.all().delete()
    KanjiRadicals.objects.all().delete()

    for character in characters:
        # basic kanji info
        jlptLevelList = character.xpath("misc/jlpt/text()")
        if jlptLevelList:
            jlptLevel = int(jlptLevelList[0])
        else:
            jlptLevel = None

        schoolGradeList = character.xpath("misc/grade/text()")
        if schoolGradeList:
            schoolGrade = int(schoolGradeList[0])
        else:
            schoolGrade = None

        frequencyList = character.xpath("misc/freq/text()")
        if frequencyList:
            frequency = int(frequencyList[0])
        else:
            frequency = None

        # store kanji to db
        kanjiDb = Kanji(
            literal=character.xpath("literal/text()")[0],
            stroke_count=int(character.xpath("misc/stroke_count/text()")[0]),
            jlpt_level=jlptLevel,
            school_grade=schoolGrade,
            frequency=frequency
        )

        kanjiDb.save()

        # radicals
        for radical in character.xpath("radical/rad_value"):
            KanjiRadicals(kanji_id=kanjiDb, radical=radical.text, type=radical.attrib.get("rad_type")).save()

        # readings
        # on
        for reading in character.xpath("reading_meaning/rmgroup/reading[@r_type='ja_on']/text()"):
            KanjiReadings(kanji_id=kanjiDb, reading=reading, type="onyomi").save()

        # kun
        for reading in character.xpath("reading_meaning/rmgroup/reading[@r_type='ja_kun']/text()"):
            KanjiReadings(kanji_id=kanjiDb, reading=reading, type="kunyomi").save()

        # nanori
        for reading in character.xpath("reading_meaning/nanori/text()"):
            KanjiReadings(kanji_id=kanjiDb, reading=reading, type="nanori").save()

        # meanings
        for meaning in character.xpath("reading_meaning/rmgroup/meaning[not(@m_lang)]/text()"):
            KanjiMeanings(kanji_id=kanjiDb, meaning=meaning, language="en-GB").save()

    return HttpResponse("all updated!")
