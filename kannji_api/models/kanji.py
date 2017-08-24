from django.db import models


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
