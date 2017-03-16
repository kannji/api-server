from django.http import JsonResponse
from django.shortcuts import get_object_or_404

from kannji_api.kanji import get_kanji_object
from kannji_api.list_model import Lists


def get_list(response, list_id):

    # get list
    list = get_object_or_404(Lists, list_id=list_id)

    responseJson = {}
    responseJson['list_id'] = list.list_id
    responseJson['name'] = list.name
    responseJson['description'] = list.description
    responseJson['thumbnail'] = list.thumbnail
    responseJson['entries'] = {}

    # add kanji to the list
    # TODO what to do with big lists?
    kanji = list.kanji.all()

    for current_kanji in kanji:
        kanjiObject = get_kanji_object(current_kanji)
        kanjiObject['type'] = 'kanji'
        responseJson['entries'][current_kanji.kanji_id] = kanjiObject

    return JsonResponse(responseJson)
