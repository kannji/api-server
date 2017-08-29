from django.conf.urls import url

from . import db_actions

urlpatterns = [
	url(r'^update/$', db_actions.update),
]
