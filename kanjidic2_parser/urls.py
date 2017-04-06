from django.conf.urls import url

from . import db_actions

urlpatterns = [
	url(r'^update/$', db_actions.updateDatabase, name='update'),
	url(r'^clear/$', db_actions.clearDatabase, name='clear'),
	url(r'^rebuild/$', db_actions.rebuildDatabase, name='rebuild'),
]
