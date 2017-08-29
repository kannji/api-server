from django.conf.urls import url, include

urlpatterns = [
	url(r'^jlpt-lists/', include('actions.jlpt-lists.urls')),
	url(r'^kanjidic2/', include('actions.kanjidic2.urls')),
	url(r'^jmdict/', include('actions.jmdict.urls')),
	url(r'^kana/', include('actions.kana.urls'))
]
