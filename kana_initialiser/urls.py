from django.conf.urls import url

from kana_initialiser import kana_initialiser

urlpatterns = [
	url(r'^initialise/$', kana_initialiser.initialise_kana, name='initialize_kana'),
]
