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


class Lists(models.Model):
    list_id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=2000, blank=True, null=True)
    thumbnail_url = models.CharField(max_length=300, blank=True, null=True)
    kanji = models.ManyToManyField(
        Kanji,
        through='ListEntries',
        through_fields=('list', 'kanji')
    )

    class Meta:
        managed = False
        db_table = 'lists'


class ListEntries(models.Model):
    entry_id = models.BigAutoField(primary_key=True)
    list = models.ForeignKey('Lists', models.DO_NOTHING)
    kanji = models.ForeignKey(Kanji, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'list_entries'
