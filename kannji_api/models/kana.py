import uuid

from django.db import models


class Kana(models.Model):
	#                            The relation of the different Kana-types
	#
	# ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓                                           ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
	# ┃     Monographs (MO)    ┃                                           ┃      Digraphs (DG)     ┃
	# ┃ ---------------------- ┃  <------ corresponding Monograph -------  ┃ ---------------------- ┃
	# ┃    plain characters    ┃                                           ┃  combined characters   ┃
	# ┃ ---------------------- ┃                                           ┃ ---------------------- ┃
	# ┃      あ, き, つ, ね     ┃                                           ┃           きょ          ┃
	# ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛                                           ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
	#             ^                                                                    ^
	#             |                                                                    |
	#       corresponding                                                        corresponding
	#         Monograph                                                             Digraph
	#             |                                                                    |
	#             |                                                                    |
	# ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓                                           ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
	# ┃     Diacritics (DC)    ┃                                           ┃ Diacritic-Digraphs (DD) ┃
	# ┃ ---------------------- ┃                                           ┃ ----------------------- ┃
	# ┃ dakuten (tenten)   [ﾞ] ┃  <------ corresponding Diacritic -------  ┃   combined characters   ┃
	# ┃ handakuten (maru)  [ﾟ] ┃                                           ┃    with (han)dakuten    ┃
	# ┃ ---------------------- ┃                                           ┃ ----------------------- ┃
	# ┃          ぎ, づ         ┃                                          ┃            ぎょ          ┃
	# ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛                                           ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
	#
	
	# abbreviations for the different kana types
	MONOGRAPH_CODE = 'MO'
	DIACRITIC_CODE = 'DC'
	DIGRAPH_CODE = 'DG'
	DIACRITIC_DIGRAPH_CODE = 'DD'
	
	# choices for the type field
	TYPE_CHOICES = (
		(MONOGRAPH_CODE, 'Monograph'),
		(DIACRITIC_CODE, 'Diacritic'),
		(DIGRAPH_CODE, 'Digraph'),
		(DIACRITIC_DIGRAPH_CODE, 'Diacritic-Digraph'),
	)
	
	# the unique id of the kana
	kana_uuid = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
	
	# the actual character
	literal = models.CharField(max_length=2, editable=False)
	
	# how you write the character in latin letters (romaji)
	transliteration = models.CharField(max_length=4)
	
	# the type of the character (monograph, diacritic, digraph, diacritic-digraph)
	type = models.CharField(max_length=2, choices=TYPE_CHOICES)
	
	# the id of the corresponding Monograph
	# e.g. for the diacritic gi (ぎ), the digraph kyo (きょ) and the diacritic-digraph (ぎょ)
	# this will hold the uuid of the monograph ki (き)
	monograph = models.ForeignKey('self', related_name='monograph_uuid', null=True)
	
	# the id of the corresponding Diacritic
	# e.g. for the diacritic-digraph gyo (ぎょ) this will hold the uuid of the diacritic ki (ぎ)
	diacritic = models.ForeignKey('self', related_name='diacritic_uuid', null=True)
	
	# the id of the corresponding Digraph
	# e.g. for the diacritic-digraph gyo (ぎょ) this will hold the uuid of the digraph ki (きょ)
	digraph = models.ForeignKey('self', related_name='digraph_uuid', null=True)
	
	def __str__(self):
		return self.literal
	
	class Meta:
		abstract = True


class Hiragana(Kana):
	corresponding_katakana = models.OneToOneField('kannji_api.Katakana', null=True)


class Katakana(Kana):
	corresponding_hiragana = models.OneToOneField('kannji_api.Hiragana', null=True)
