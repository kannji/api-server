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
	kana_id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
	
	# the actual character
	literal = models.CharField(max_length=1)
	
	# how you write the character in latin letters (romaji)
	transliteration = models.CharField(max_length=4)
	
	# the type of the character (monograph, diacritic, digraph, diacritic-digraph)
	type = models.CharField(max_length=2, choices=TYPE_CHOICES)
	
	def __str__(self):
		return self.literal

	class Meta:
		abstract = True

class Hiragana(Kana):
	# the id of the corresponding Monograph
	# e.g. for the diacritic gi (ぎ), the digraph kyo (きょ) and the diacritic-digraph (ぎょ)
	# this will hold the uuid of the monograph ki (き)
	monograph = models.ForeignKey('self', related_name='monograph_uuid')

	# the id of the corresponding Diacritic
	# e.g. for the diacritic-digraph gyo (ぎょ) this will hold the uuid of the diacritic ki (ぎ)
	diacritic = models.ForeignKey('self', related_name='diacritic_uuid')

	# the id of the corresponding Digraph
	# e.g. for the diacritic-digraph gyo (ぎょ) this will hold the uuid of the digraph ki (きょ)
	digraph = models.ForeignKey('self', related_name='digraph_uuid')
	
	corresponding_katakana = models.ForeignKey('kannji_api.Katakana')


class Katakana(Kana):
	# the id of the corresponding Monograph
	# e.g. for the diacritic gi (ギ), the digraph kyo (キョ) and the diacritic-digraph (ギョ)
	# this will hold the uuid of the monograph ki (キ)
	monograph = models.ForeignKey('self', related_name='monograph_uuid')

	# the id of the corresponding Diacritic
	# e.g. for the diacritic-digraph gyo (ギョ) this will hold the uuid of the diacritic ki (ギ)
	diacritic = models.ForeignKey('self', related_name='diacritic_uuid')

	# the id of the corresponding Digraph
	# e.g. for the diacritic-digraph gyo (ギョ) this will hold the uuid of the digraph ki (キョ)
	digraph = models.ForeignKey('self', related_name='digraph_uuid')
	
	corresponding_hiragana = models.ForeignKey('kannji_api.Hiragana')


class Kanji(models.Model):
	kanji_id = models.BigAutoField(primary_key=True)
	literal = models.CharField(max_length=1)
	stroke_count = models.PositiveSmallIntegerField()
	jlpt_level = models.PositiveSmallIntegerField(null=True)
	school_grade = models.PositiveSmallIntegerField(null=True)
	frequency = models.PositiveSmallIntegerField(null=True)
	
	def __str__(self):
		return self.literal


class KanjiMeanings(models.Model):
	meaning_id = models.BigAutoField(primary_key=True)
	kanji = models.ForeignKey(Kanji, related_name='kanji_meanings_set', on_delete=models.CASCADE)
	meaning = models.CharField(max_length=200, null=True)
	language = models.CharField(max_length=7, null=True)
	
	class Meta:
		unique_together = (('meaning_id', 'kanji'), ('kanji', 'meaning', 'language'),)
	
	def __str__(self):
		return self.meaning


class KanjiReadings(models.Model):
	reading_id = models.BigAutoField(primary_key=True)
	kanji = models.ForeignKey(Kanji, related_name='kanji_readings_set', on_delete=models.CASCADE)
	reading = models.CharField(max_length=20)
	type = models.CharField(max_length=7)
	
	class Meta:
		unique_together = (('reading_id', 'kanji'), ('kanji', 'reading', 'type'),)
	
	def __str__(self):
		return self.reading


class KanjiRadicals(models.Model):
	radical_id = models.BigAutoField(primary_key=True)
	kanji = models.ForeignKey(Kanji, related_name='kanji_radicals_set', on_delete=models.CASCADE)
	radical = models.PositiveSmallIntegerField()
	type = models.CharField(max_length=20)
	
	class Meta:
		unique_together = (('radical_id', 'kanji'), ('kanji', 'radical', 'type'),)
	
	def __str__(self):
		return self.radical


class LearningLists(models.Model):
	list_id = models.BigAutoField(primary_key=True)
	kanji = models.ManyToManyField(Kanji)
	name = models.CharField(max_length=200)
	description = models.CharField(max_length=2000, null=True)
	thumbnail_url = models.CharField(max_length=300, null=True)
