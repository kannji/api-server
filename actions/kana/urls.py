from django.conf.urls import url

from actions.kana import kana

urlpatterns = [
	url(r'^initialise/$', kana.initialise),
]
