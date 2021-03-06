import time

from django.db import connection
from django.http import HttpResponse
from lxml import etree

from kannji_api.models import Kanji, KanjiReadings, KanjiMeanings, KanjiRadicals
from parser.parsing_helper import xpathGetInt, xpathGetStr


def clear_database(request):
	Kanji.objects.all().delete()
	KanjiMeanings.objects.all().delete()
	KanjiReadings.objects.all().delete()
	KanjiRadicals.objects.all().delete()
	
	with connection.cursor() as cursor:
		cursor.execute("ALTER TABLE `kanji` AUTO_INCREMENT = 1;")
		cursor.execute("ALTER TABLE `kanji_meanings` AUTO_INCREMENT = 1;")
		cursor.execute("ALTER TABLE `kanji_readings` AUTO_INCREMENT = 1;")
		cursor.execute("ALTER TABLE `kanji_radicals` AUTO_INCREMENT = 1;")


def rebuild_database(request):
	clear_database(request)
	return update_database(request)


def add_kanji_from_xml(literal, character):
	# get all kanji info
	stroke_count = xpathGetInt(character, "misc/stroke_count")
	jlpt_level = xpathGetInt(character, "misc/jlpt")
	school_grade = xpathGetInt(character, "misc/grade")
	frequency = xpathGetInt(character, "misc/freq")
	
	# add the kanji to the db
	kanji = Kanji(
		literal=literal,
		stroke_count=stroke_count,
		jlpt_level=jlpt_level,
		school_grade=school_grade,
		frequency=frequency
	)
	kanji.save()
	
	if Kanji.objects.filter(literal=literal).exists():
		# add foreign info
		# radicals
		for radical in character.xpath("radical/rad_value"):
			KanjiRadicals(kanji=kanji, radical=radical.text, type=radical.attrib.get("rad_type")).save()
		
		# readings
		# on
		for reading in character.xpath("reading_meaning/rmgroup/reading[@r_type='ja_on']/text()"):
			KanjiReadings(kanji=kanji, reading=reading, type="onyomi").save()
		
		# kun
		for reading in character.xpath("reading_meaning/rmgroup/reading[@r_type='ja_kun']/text()"):
			KanjiReadings(kanji=kanji, reading=reading, type="kunyomi").save()
		
		# nanori
		for reading in character.xpath("reading_meaning/nanori/text()"):
			KanjiReadings(kanji=kanji, reading=reading, type="nanori").save()
		
		# meanings
		for meaning in character.xpath("reading_meaning/rmgroup/meaning[not(@m_lang)]/text()"):
			KanjiMeanings(kanji=kanji, meaning=meaning, language="en-GB").save()
		
		return True
	else:
		# adding kanji didn't work, so we delete it. (fuck you encoding)
		kanji.delete()
		return False


def update_kanji_from_xml(literal, character):
	# TODO: actually update the kanji
	pass


def update_database(request):
	# some statistics
	start_time = time.time()
	update_count = 0
	update_list = []
	add_count = 0
	added_list = []
	skip_count = 0
	skip_list = []
	
	# looping through all characters (kanji) in xml file
	# i = 0
	for event, character in etree.iterparse("kanjidic2_parser/kanjidic2.xml", tag="character"):
		# i += 1
		# if i > 10:
		#    break
		
		# get literal and have a look what to do with it
		literal = xpathGetStr(character, "literal")
		
		# try getting the kanji from db
		if Kanji.objects.filter(literal=literal).exists():
			update_kanji_from_xml(literal, character)
			update_count += 1
			update_list.append(literal)
		else:
			kanji_added = add_kanji_from_xml(literal, character)
			if kanji_added:
				add_count += 1
				added_list.append(literal)
			else:
				skip_count += 1
				skip_list.append(literal)
		
		# clear the character to save ram
		character.clear()
	
	# some statistics
	end_time = time.time()
	
	return HttpResponse(
		'updated:' + str(update_count) + '<br>\n' +
		'added:' + str(add_count) + '<br>\n' +
		'skipped:' + str(skip_count) + '<br>\n' +
		'Time needed: ' + str(end_time - start_time) + '<br><br>\n' +
		'updated kanji: <br>\n' +
		', '.join(update_list) + '<br><br>\n' +
		'addded kanji: <br>\n' +
		', '.join(added_list) + '<br><br>\n' +
		'skipped kanji: <br>\n' +
		', '.join(skip_list) + '<br><br>\n'
	)
