from actions.kana import kana_list
from kannji_api.models.kana import Hiragana, Katakana


def initialise(request):
	for kana in kana_list:
		curr_hiragana = Hiragana(
			literal=kana['hiragana_literal'],
			transliteration=kana['transliteration'],
			type=kana['type']
		)
		curr_hiragana.save()
		
		curr_katakana = Katakana(
			literal=kana['katakana_literal'],
			transliteration=kana['transliteration'],
			type=kana['type'],
			corresponding_hiragana=curr_hiragana
		)
		curr_katakana.save()
		
		curr_hiragana.corresponding_katakana = curr_katakana
		curr_hiragana.save()
	
	# TODO: make connections to the corresponding monograph. digraph adn diacritic
