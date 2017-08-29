from django.conf.urls import url

from . import jlpt_list_creator

urlpatterns = [
	url(r'^create/$', jlpt_list_creator.create_jlpt_lists, name='index'),
]
