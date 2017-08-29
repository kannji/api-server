from django.conf.urls import url

from . import kanjidic2

urlpatterns = [
	url(r'^update/$', kanjidic2.update_database, name='update'),
	url(r'^clear/$', kanjidic2.clear_database, name='clear'),
	url(r'^rebuild/$', kanjidic2.rebuild_database, name='rebuild'),
]
