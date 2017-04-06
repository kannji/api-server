from django.conf.urls import url

from . import jlpt_list_creator

urlpatterns = [
	url(r'^$', jlpt_list_creator.createJlptLists, name='index'),
]
