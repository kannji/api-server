# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from __future__ import unicode_literals

from django.db import models

class Kanji(models.Model):
    kanji_id = models.BigAutoField(primary_key=True)
    literal = models.CharField(max_length=1)
    stroke_count = models.PositiveSmallIntegerField()
    jlpt_level = models.PositiveSmallIntegerField()
    school_grade = models.PositiveSmallIntegerField()
    frequency = models.PositiveSmallIntegerField()

    class Meta:
        managed = False
        db_table = 'kanji'

    def __str__(self):
        return self.literal


class KanjiMeanings(models.Model):
    meaning_id = models.BigAutoField(primary_key=True)
    kanji_id = models.ForeignKey(Kanji, db_column='kanji_id', related_name='kanji_meanings_set', on_delete=models.CASCADE)
    meaning = models.CharField(max_length=200, blank=True, null=True)
    language = models.CharField(max_length=7, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'kanji_meanings'
        unique_together = (('meaning_id', 'kanji_id'), ('kanji_id', 'meaning', 'language'),)

    def __str__(self):
        return self.meaning


class KanjiReadings(models.Model):
    reading_id = models.BigAutoField(primary_key=True)
    kanji_id = models.ForeignKey(Kanji, db_column='kanji_id', related_name='kanji_readings_set', on_delete=models.CASCADE)
    reading = models.CharField(max_length=20)
    type = models.CharField(max_length=7)

    class Meta:
        managed = False
        db_table = 'kanji_readings'
        unique_together = (('reading_id', 'kanji_id'), ('kanji_id', 'reading', 'type'),)

    def __str__(self):
        return self.reading

class KanjiRadicals(models.Model):
    radical_id = models.BigAutoField(primary_key=True)
    kanji_id = models.ForeignKey(Kanji, db_column='kanji_id', related_name='kanji_radicals_set', on_delete=models.CASCADE)
    radical = models.PositiveSmallIntegerField()
    type = models.CharField(max_length=20)

    class Meta:
        managed = False
        db_table = 'kanji_radicals'
        unique_together = (('radical_id', 'kanji_id'), ('kanji_id', 'radical', 'type'),)

    def __str__(self):
        return self.radical
