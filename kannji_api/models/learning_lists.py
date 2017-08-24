from django.db import models
from kannji_api.models import Kanji


class LearningLists(models.Model):
	list_id = models.BigAutoField(primary_key=True)
	kanji = models.ManyToManyField(Kanji)
	name = models.CharField(max_length=200)
	description = models.CharField(max_length=2000, null=True)
	thumbnail_url = models.CharField(max_length=300, null=True)
