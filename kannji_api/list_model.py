# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from __future__ import unicode_literals

from django.db import models

from kannji_api.kanji_model import Kanji


class LearningLists(models.Model):
	list_id = models.BigAutoField(primary_key=True)
	kanji = models.ManyToManyField(Kanji)
	name = models.CharField(max_length=200)
	description = models.CharField(max_length=2000, blank=True, null=True)
	thumbnail_url = models.CharField(max_length=300, blank=True, null=True)
