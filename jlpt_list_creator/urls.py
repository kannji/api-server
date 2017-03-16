from django.conf.urls import url

from jlpt_list_creator import jlpt_list_creator
from . import jlpt_list_creator

urlpatterns = [
    url(r'^$', jlpt_list_creator.createJlptLists, name='index'),
]
