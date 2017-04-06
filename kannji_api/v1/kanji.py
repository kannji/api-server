from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404

from kannji_api.kanji_model import Kanji


def index(request):
	return HttpResponse("Hello, you are at the Kannji api index.")


def search_kanji(request, searchQuery, maxResults):
	kanji = Kanji.objects.filter(literal__search=searchQuery)[:5]
	
	""""
	SELECT kanji.kanji_id, kanji.literal, kanji_readings.reading, kanji_meanings.meaning
	FROM kanji
	RIGHT JOIN kanji_readings
		ON kanji.kanji_id = kanji_readings.kanji_id
	RIGHT JOIN kanji_meanings
		ON kanji.kanji_id = kanji_meanings.kanji_id
	WHERE
		kanji.literal LIKE "to go" OR
		kanji_readings.reading LIKE "to go" OR
		kanji_meanings.meaning LIKE "to go"
	"""


def get_all_kanji(request):
	responseJson = {}
	
	kanjis = Kanji.objects.all()
	
	for kanji in kanjis:
		responseJson[kanji.kanji_id] = get_kanji_object(kanji)
	
	return JsonResponse(responseJson)


def get_kanji(response, kanji_id):
	kanji = get_object_or_404(Kanji, kanji_id=kanji_id)
	return JsonResponse(get_kanji_object(kanji))


def get_random_kanji(response):
	kanji = Kanji.objects.order_by('?').first()
	return JsonResponse(get_kanji_object(kanji))


def get_kanji_object(kanji):
	responseJson = {}
	
	# getting Kanji information
	responseJson['kanji_id'] = kanji.kanji_id
	responseJson['literal'] = kanji.literal
	responseJson['stroke_count'] = kanji.stroke_count
	
	# getting the readings
	readings = kanji.kanji_readings_set.all()
	
	responseJson['readings'] = {}
	
	for reading in readings:
		responseJson['readings'][reading.reading_id] = {}
		responseJson['readings'][reading.reading_id]['reading'] = reading.reading
		responseJson['readings'][reading.reading_id]['type'] = reading.type
	
	# getting the meanings
	meanings = kanji.kanji_meanings_set.all()
	
	responseJson['meanings'] = {}
	
	for meaning in meanings:
		responseJson['meanings'][meaning.meaning_id] = {}
		responseJson['meanings'][meaning.meaning_id]['meaning'] = meaning.meaning
		responseJson['meanings'][meaning.meaning_id]['language'] = meaning.language
	
	return responseJson
